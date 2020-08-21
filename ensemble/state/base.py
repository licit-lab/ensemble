""" 
    This module contains a base class definition representing a single generic state
"""


class State(object):
    """
        This class defines a state object which provides basic functionalities for individual states within the state machine. 
    """

    def __init__(self):
        print("State:", str(self))

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
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


class PlatoonState(object):
    """
        This class defines a state object for a platoon which provides basic functionalities for individual states within the state machine. 
    """

    def __init__(self):
        print("State:", str(self))

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
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
