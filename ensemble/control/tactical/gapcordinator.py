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

PLState = Union[StandAlone, Platooning, Joining, Splitting]

MAXTRKS = DCT_PLT_CONST["max_platoon_length"]
MAXNDST = DCT_PLT_CONST["max_connection_distance"]


@dataclass
class FrontGap:

    status: PLState = StandAlone()
    platoon: bool = False
    comv2x: bool = True

    def __init__(self, vehicle: Vehicle = None):
        self.vehicle = vehicle


@dataclass
class RearGap:
    def __init__(self, vehicle: Vehicle = None):
        self.vehicle = vehicle


@dataclass
class VehGapCoordinator:
    def __init__(self, vehicle: Vehicle):
        self.ego = vehicle
        self._fgc = FrontGap(self.ego)
        self._rgc = RearGap(self.ego)
        self._platoonid = 0

    def __hash__(self):
        return hash((type(self), self.ego.vehid))

    @property
    def x(self):
        """ Ego current position in link """
        return self.ego.distance

    @property
    def leader(self):
        """ Returns the leader vehicle in the platoon"""
        return self._fgc.vehicle if self._fgc.vehicle is not None else self.ego

    @property
    def follower(self):
        """ Returns the follower vehicle in the platoon"""
        return self._fgc.vehicle if self._fgc.vehicle is not None else self.ego

    @property
    def is_head(self):
        """ Determines if the vehicle is head of the platoon"""
        return self.leader is self.ego

    @property
    def is_tail(self):
        """ Determines if the vehicle is tail of the platoon """
        return self.follower is self.ego

    @property
    def dx(self):
        """ Ego current headway space"""
        return self.leader.ttd - self.ego.ttd

    @property
    def pid(self):
        """ Platoon id 0-index notation to denote position on the platoon"""
        return self._platoonid

    @property
    def joinable(self):
        return (self.pid < MAXTRKS) and (self.dx < MAXNDST) and self._fgc.comv2x


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
