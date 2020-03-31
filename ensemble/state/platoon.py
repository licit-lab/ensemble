""" 
    This module defines the basic states required to determine the status of a vehicle in a platoon formation

    The states are defined as: 

    * **StandAlone**: Vehicle not in a platoon formation
    * **Join**: Vehicle willing to join a platoon or willing to create a platoon 
    * **Platooning**: Vehicle inside a platoon formation 
    * **CutIn**: Vehicle has detected an intruder in the formation
    * **CutThrough**: Vehicle has detected an intruder in the formation
    * **Split**: Vehicle is willing to split from current platoon. 

"""

from .base import PlatoonState


class StandAlone(PlatoonState):
    """
    The state which declares the vehicle in stand alone mode
    """

    def switchto(self, event):

        if event == "join":
            return Join()
        else:
            return self


class Join(PlatoonState):
    """
    The state which declares the vehicle in joining a platoon 
    """

    def switchto(self, event):

        if event == "platoon":
            return Platoon()
        else:
            return self


class Platoon(PlatoonState):
    """
    The state which declares the vehicle in a platoon 
    """

    def switchto(self, event):

        if event == "cutin":
            return CutIn()
        elif event == "split":
            return Split()
        else:
            return self


class CutIn(PlatoonState):
    """
    The state which declares the vehicle reacting to cut-in
    """

    def switchto(self, event):

        if event == "cutthrough":
            return CutThrough()
        elif event == "split":
            return Split()
        else:
            return self


class CutThrough(PlatoonState):
    """
    The state which declares the vehicle reacting to cut-through
    """

    def switchto(self, event):

        if event == "platoon":
            return Platoon()
        else:
            return self


class Split(PlatoonState):
    """
    The state which declares the vehicle splitting from platoon 
    """

    def switchto(self, event):

        if event == "standalone":
            return StandAlone()
        else:
            return self
