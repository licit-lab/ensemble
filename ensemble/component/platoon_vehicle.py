"""
Platoon Vehicle
===============
This module contains information on a vehicle platoon. 

The platoon vehicle model acts as an instance to trace individual vehicle data and modify vehicle behavior according to given dynamics. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

# from ensemble.component.vehicles import Vehicle

from dataclasses import dataclass
from symupy.components import Vehicle

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


from ensemble.tools.constants import DCT_PLT_CONST

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class PlatoonVehicle(Vehicle):
    """This is a vehicle class defined for storing data of a single platoon
    vehicle.

    You need a Publisher from where the vehicle is going to take data:

    Args:
        request (Publisher): Parser or object publishing data

    Retunrns:
        vehicle (Vehicle): A Dataclass with vehicle parameters

    ============================  =================================
    **Variable**                  **Description**
    ----------------------------  ---------------------------------
    ``abscissa``                    Current coordinate on y axis
    ``acceleration``                Current acceleration
    ``distance``                    Current distance traveled on link
    ``elevation``                   Current elevation
    ``lane``                        Current lane
    ``link``                        Current road vehicle is traveling
    ``ordinate``                    Current coordinate x axis
    ``speed``                       Current speed
    ``vehid``                       Vehicle id
    ``vehtype``                     Vehicle class
    ============================  =================================

    Example:
        This is one example on how to register a new vehicle ::

        >>> req = SimulatorRequest()
        >>> veh = Vehicle(req)
        >>> req.dispatch() # This will update vehicle data

    When having multiple vehicles please indicate the `vehid` before launching the dispatch method. This is because the vehicle object is looks for a vehicle id within the data.

    Example:
        This is one example on how to register two vehicles ::

        >>> req = SimulatorRequest()
        >>> veh1 = Vehicle(req, vehid=0)
        >>> veh2 = Vehicle(req, vehid=1)
        >>> req.dispatch() # This will update vehicle data on both vehicles

    """

    ego_position: int = 1
    platoon_length: int = 1
    desired_platoon_speed: float = 20
    maximum_speed: float = 25
    maximum_acceleration: float = 2.0
    maximum_deceleration: float = -2.0
    state: str = "STANDALONE"
    intruder: bool = False
    split_request: bool = False

    def joinable(self):
        if (self.leader.ego_position() < DCT_PLT_CONST["max_platoon_length"]) and (
            self.gap_distance_error() < DCT_PLT_CONST["max_connection_distance"]
        ):
            return True
        else:
            return False

    def relative_speed(self):
        speed_diff = self.speed - self.leader.speed
        return speed_diff

    def gap_distance_error(self):
        gap = self.leader.posX - self.posX - self.leader.length
        return gap

    def distance_to_leader(self):
        dist = self.leader.posX - self.posX

    def join_request(self):
        if self.leader.joinable() == True:
            return True
        else:
            return False

    def cancel_join_request(self):  # add lane change and other conditions
        if self.leader.is_platoon_vehicle() == False:
            return True
        else:
            return False

    def confirm_platoon(self):
        if (self.relative_speed() < DCT_PLT_CONST["max_platoon_length"]) and (
            self.gap_distance_error() < DCT_PLT_CONST["max_gap_distance_error"]
        ):
            self.state = "PLATOON"
            self.ego_position = self.leader.ego_position + 1  # update position

    def platoon_split(self):
        if (
            ((self.leader.is_platoon_vehicle() == False))
            or (self.split_request() == True)
            or (self.leader.split_request() == True)
        ):
            return True

    def rejoin_platoon(self):
        if (
            (self.split_request() == False)
            and (self.distance_to_leader < DCT_PLT_CONST["standalone_gap"])
            and (self.leader.is_platoon_vehicle() == False)
        ):
            return True
        else:
            return False

    def leave_platoon(self, platoonvehicle):
        if platoonvehicle.distance_to_leader > DCT_PLT_CONST["standalone_gap"]:
            return True
        else:
            return False
