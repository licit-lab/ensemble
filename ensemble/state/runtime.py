"""
    This module describes classes and objects to perform a runtime of a single scenario
"""

from itertools import chain
import click

from .states import Compliance, Connect, Initialize, PreRoutine, Query, Control, Push, PostRoutine, Terminate


start_seq = ["compliance", "connect", "initialize"]
runtime_seq = ["preroutine", "query", "control", "push", "postroutine"]
end_seq = [
    "terminate",
]


class RuntimeDevice(object):
    """ This class defines the runtime device describing a series of cyclic states required to be run 

    :param object: [description]
    :type object: [type]
    """

    def __init__(self, configurator):
        self.state = Compliance()  # Initial state
        self.configurator = configurator
        self.cycles = configurator.total_steps

    def __enter__(self) -> None:
        """ Implementation of the state machine         
        """
        full_seq = chain(start_seq, self.cycles * runtime_seq, end_seq)

        ccycle = 0
        for event in full_seq:
            self.on_event(event)
            if isinstance(self.state, PreRoutine):  # Step counted on PreRoutine
                ccycle = ccycle + 1
                click.echo(click.style(f"Step: {ccycle}", fg="cyan", bold=True))

        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    def on_event(self, event):
        """ Action to consider on event:

        * compliance
        * connect
        * initialize
        * preroutine
        * query
        * control
        * push
        * postroutine
        * terminate
        
        :param event: 
        :type event: [type]
        """
        self.state = self.state.on_event(event)
