""" 
    This module defines the basic states required to determine the status of a vehicle in a platoon formation

    The states are defined as: 

    * **StandAlone**: Vehicle not in a platoon formation
    * **Join**: Vehicle willing to join a platoon or willing to create a platoon 
    * **Platooning**: Vehicle inside a platoon formation
    * **Split**: Vehicle is willing to split from current platoon.

"""

from .base import PlatoonState


class StandAlone(PlatoonState):
    """
    The state which declares the vehicle in stand alone mode.
    A vehicle can move from StandAlone to Join
    """

    def switchto(self, event):

        if event == "join":
            return Join()
        else:
            return self


class Join(PlatoonState):
    """
    The state which declares the vehicle in joining a platoon.
    A vehicle can move from Join state to platoon state
    """

    def switchto(self, event):

        if event == "platoon":
            return Platoon()
        elif event=="standalone": # caused by cutin during joining
            return StandAlone()
        else:
            return self


class Platoon(PlatoonState):
    """
    The state which declares the vehicle in a platoon
    A vehicle can move from platoon to split because of  cut-in(intruder) or to a split(requested  by ego vehicle or front target)
    """

    def switchto(self, event):

        if event=="split":
            return Split()
        else:
            return self


class Split(PlatoonState):
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def switchto(self, event):

        if event == "platoon":
            return Platoon()
        elif event == "standalone":
            return StandAlone()
        else:
            return self
