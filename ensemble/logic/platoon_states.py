""" 
    This module defines the basic states required to determine the status of a vehicle in a platoon formation

    The states are defined as: 

    * **StandAlone**: Vehicle not in a platoon formation
    * **Joining**: Vehicle willing to join a platoon or willing to create a platoon 
    * **Platooning**: Vehicle inside a platoon formation
    * **Split**: Vehicle is willing to split from current platoon.

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ensemble.metaclass.state import AbsState
from ensemble.metaclass.coordinator import AbsSingleGapCoord

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class StandAlone(AbsState):
    """The state which declares the vehicle in stand alone mode.

    Note:
        Transition: `StandAlone` to `Joining`

    """

    def next_state(self, vgc: AbsSingleGapCoord):
        """Determines the switching condition for the state:

        Note:
            Transition: `StandAlone` to `Joining`

        Args:
            truck (fgc): Platoon vehicle containing information of the ego vehicle.

        """
        if vgc.joinable:
            return Joining().next_state(vgc)
        else:
            return self


class Joining(AbsState):
    """The state which declares the vehicle in joining a platoon.

    Note:
        Transition: `Joining` to `StandAlone`
        Transition: `Joining` to `Platooning`
    """

    def next_state(self, vgc: AbsSingleGapCoord):
        """Determines the switching condition for the state:

        Note:
            Transition: `Joining` to `StandAlone`
            Transition: `Joining` to `Platooning`

        Args:
            truck (vehicle): Platoon vehicle containing information of the ego vehicle.

        """
        if vgc.cancel_join_request(False):
            return StandAlone()
        elif vgc.confirm_platoon():
            return Platooning()
            # vehicle.ego_position = (
            #     platoonvehicle.leader.ego_position + 1
            # )  # update position in platoon
            # platoonvehicle.state = "PLATOON"  # update  vehicle state
        else:
            return self


class Splitting(AbsState):
    """The state which declares the vehicle splitting from platoon

    Note:
        Transition: `Splitting` to `StandAlone`
        Transition: `Splitting` to `Platooning`

    """

    def next_state(self, vehicle):
        """Determines the switching condition for the state:

        Note:
            Transition: `Splitting` to `StandAlone`
            Transition: `Splitting` to `Platooning`

        Args:
            truck (vehicle): Platoon vehicle containing information of the ego vehicle.

        """

        if vehicle.rejoin_platoon():
            return Platooning()
        elif vehicle.leave_platoon():
            return StandAlone()
        else:
            return self


class Platooning(AbsState):
    """The state which declares the vehicle in a platoon functionality

    Note:
        Transition: `Platooning` to `Splitting`
    """

    def next_state(self, vehicle):
        """Determines the switching condition for the state:

        Note:
            Transition: `Platooning` to `Splitting`

        Args:
            truck (vehicle): Platoon vehicle containing information of the ego vehicle.

        """
        if vehicle.platoon_split():
            return Splitting()
        else:
            return self


class Cutin(AbsState):
    """The state which declares the vehicle in a platoon functionality

    Note:
        Transition: `Cutin` to `Splitting`
    """

    def next_state(self, vehicle):
        """Determines the switching condition for the state:

        Note:
            Transition: `Platooning` to `Splitting`

        Args:
            truck (vehicle): Platoon vehicle containing information of the ego vehicle.

        """
        if vehicle.cutin():
            return Splitting()
        else:
            return self


# class BackSplit(AbsState):
#     """
#     The state which declares the vehicle splitting from platoon
#     A vehicle can move from split to platoon or to standalone
#     """

#     def next_state(self, vehicle):

#         if vehicle.rejoin_platoon() == True:
#             return Platooning()
#         elif vehicle.leave_platoon() == True:
#             return StandAlone()
#         else:
#             return self
