"""
    This module describes classes and objects to perform a runtime of a single scenario
"""

from itertools import chain
import click

from .states import (
    Compliance,
    Connect,
    Initialize,
    PreRoutine,
    Query,
    Control,
    Push,
    PostRoutine,
    Terminate,
)


START_SEQ = ["compliance", "connect", "initialize"]
RUNTIME_SEQ = ["preroutine", "query", "control", "push", "postroutine"]
END_SEQ = [
    "terminate",
]


class RuntimeDevice:
    """ This class defines the runtime device describing a series of 
        cyclic states required to be run:

    """

    def __init__(self, configurator):
        self.state = Compliance()  # Initial state
        self.configurator = configurator
        self.cycles = configurator.total_steps

    def __enter__(self) -> None:
        """ Implementation of the state machine         
        """
        full_seq = chain(START_SEQ, self.cycles * RUNTIME_SEQ, END_SEQ)

        ccycle = 0
        for event in full_seq:
            self.on_event(event)
            if isinstance(self.state, PostRoutine):  # Step counted on PreRoutine
                ccycle = ccycle + 1
                click.echo(click.style(f"Step: {ccycle}", fg="cyan", bold=True))
            if isinstance(self.state, Terminate):
                break

        self.on_event(event)  # Run Terminate sequence

        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    def on_event(self, event: str):
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
        :type event: str 
        :param configurator:
        :type configurator: Configurator
        """
        self.state = self.state.on_event(event, self.configurator)
