"""
Runtime Device
=================
This module describes classes and objects to perform a runtime of a single scenario
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from itertools import chain
import click

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .runtime_states import (
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

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


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
            self.next_state(event)
            # Step counted on PreRoutine
            if isinstance(self.state, PostRoutine):
                ccycle = ccycle + 1
                click.echo(click.style(f"Step: {ccycle}", fg="cyan", bold=True))
            if isinstance(self.state, Terminate):
                break
 
        self.next_state(event)  # Run Terminate sequence

        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    def next_state(self, event: str):
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
        self.state = self.state.next_state(event, self.configurator)
