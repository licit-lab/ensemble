"""
States 
==========
This module presents a state implementation that should be generic for state descriptions.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class AbsState(metaclass=abc.ABCMeta):
    def __init__(self):
        print("State:", str(self))

    @abc.abstractmethod
    def on_event(self):
        """ State to switch on event"""
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__
