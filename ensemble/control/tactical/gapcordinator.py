"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

from itertools import groupby

from dataclasses import dataclass

from typing import Union

from ensemble.control.tactical.frontandreargap import Platoon
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)
from ensemble.component.vehiclelist import VehicleList
from ensemble.component.vehicle import Vehicle
from ensemble.logic.platoon_set import PlatoonSet
from ensemble.tools.constants import DCT_PLT_CONST

PLState = Union[StandAlone,Platooning,Joining,Splitting]
@dataclass
class FrontGap:

    status: PLState = StandAlone()
    platoon: bool = False
    comv2x: bool = True

    def __init__(self, vehicle: Vehicle):
        self.leader = None
        # Platoon state

@dataclass
class RearGap:
    def __init__(self, vehicle: Vehicle):
        self.follower = None


@dataclass
class VehGapCoordinator:
    def __init__(self, vehicle: Vehicle):
        self.ego = vehicle
        self._fcg = FrontGap(self.ego)
        self._rgc = RearGap(self.ego)

@dataclass
class GlobalGapCoordinator:
    def __init__(self, vehicle_registry: VehicleList):
        self._gclist = [
            VehGapCoordinator(veh)
            for veh in vehicle_registry
            if veh.vehtype in DCT_PLT_CONST.get("platoon_types")
        ]
        self._platoons = []

    def solve_platoons(self):

        # This grooups vehicles per road type
        vtf = lambda x: x.ego.link

        # Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gclist, vtf):
            for gc in group_gc:
                if len(self._platoons) >= 1:
                    tmp = self._platoons[-1] + PlatoonSet(gc)
                    if len(tmp) > self._platoons[-1]:
                        self._platoons[-1] = tmp
                    else:
                        self._platoons.append(PlatoonSet(gc))
                else:
                    self._platoons.append(PlatoonSet((gc,)))



# class FrontGap(Subscriber, StateMachine):
#     def __init__(self, veh=PlatoonVehicle()):
#         if veh.state == "STANDALONE":
#             self.currentState = StandAlone()
#         elif veh.state == "JOIN":
#             self.currentState = Join()
#         elif veh.state == "PLATOON":
#             self.currentState = Platoon()
#         else:
#             self.currentState = Split()

#     def update_front(self, vehicle_env):
#         """ update informatino from ego vehicle + leader"""
#         self.ego = vehicle_env["ego"]
#         self.leader = vehicle_env["leader"]


# class RearGap(Subscriber, StateMachine):
#     def __init__(self, veh=PlatoonVehicle()):
#         if veh.follower().state == "STANDALONE":
#             self.currentState = StandAlone()
#         elif veh.follower().state == "JOIN":
#             self.currentState = Join()
#         elif veh.follower().state == "PLATOON":
#             self.currentState = Platoon()
#         else:
#             self.currentState = Split()

#     def update_back(self, vehicle_env):
#         """ update informatino from ego vehicle + follower"""
#         self.ego = vehicle_env["ego"]
#         self.back = vehicle_env["follower"]
