""" 
    This module defines the basic states required to determine the status of a vehicle in a platoon formation

    The states are defined as: 

    * **StandAlone**: Vehicle not in a platoon formation
    * **Join**: Vehicle willing to join a platoon or willing to create a platoon 
    * **Platooning**: Vehicle inside a platoon formation
    * **Split**: Vehicle is willing to split from current platoon.

"""
from ensemble.component.platoonvehicle import PlatoonVehicle
from .base import PlatoonState


class StandAlone(PlatoonState):
    """
    The state which declares the vehicle in stand alone mode.
    A vehicle can move from StandAlone to Join
    """

    def run(self):
        print("StandAloneMode")

    def next_state(self, platoonvehicle=PlatoonVehicle()):
        if platoonvehicle.leader.joinable() == True:
            return Join()
        else:
            return self


class Join(PlatoonState):
    """
    The state which declares the vehicle in joining a platoon.
    A vehicle can move from Join state to platoon state
    """

    def run(self):
        print("JoinMode")

    def next_state(self, platoonvehicle=PlatoonVehicle()):
        if platoonvehicle.cancel_join_request() == True:
            return StandAlone()
        elif platoonvehicle.confirm_platoon() == True:
            platoonvehicle.ego_position = platoonvehicle.leader.ego_position + 1  # update position in platoon
            platoonvehicle.state = "PLATOON"  # update  vehicle state
            return Platoon()
        else:
            return self


class Platoon(PlatoonState):
    """
    The state which declares the vehicle in a platoon
    A vehicle can move from platoon to split because of  cut-in(intruder) or to a split(requested  by ego vehicle or front target)
    """

    def run(self):
        print("PlatoonMode")

    def next_state(self, platoonvehicle=PlatoonVehicle()):
        if platoonvehicle.platoon_split() == True:
            return Split()
        else:
            return self


class Split(PlatoonState):
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def next_state(self, platoonvehicle=PlatoonVehicle()):

        if platoonvehicle.rejoin_platoon() == True:
            return Platoon()
        elif platoonvehicle.leave_platoon() == True:
            return StandAlone()
        else:
            return self


class BackSplit(PlatoonState):
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def next_state(self, platoonvehicle=PlatoonVehicle()):

        if platoonvehicle.rejoin_platoon() == True:
            return Platoon()
        elif platoonvehicle.leave_platoon() == True:
            return StandAlone()
        else:
            return self
