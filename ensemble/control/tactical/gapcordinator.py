"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

import numpy as np

from itertools import groupby

from dataclasses import dataclass

from typing import Union

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
    def __init__(
        self, vehicle: Vehicle, leader: Vehicle = None, follower: Vehicle = None
    ):
        self.ego = vehicle
        self._fgc = FrontGap(leader)
        self._rgc = RearGap(follower)
        self.pid = 0

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
        return self._rgc.vehicle if self._rgc.vehicle is not None else self.ego

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
        return (
            self.leader.ttd - self.ego.ttd
            if self.leader.vehid != self.ego.vehid
            else MAXNDST
        )

    @property
    def pid(self):
        """ Platoon id 0-index notation to denote position on the platoon"""
        return self._platoonid

    @pid.setter
    def pid(self, value):
        """ Platoon id 0-index"""
        self._platoonid = np.clip(value, 0, MAXTRKS)

    @property
    def joinable(self):
        return (self.pid < MAXTRKS) and (self.dx < MAXNDST) and self._fgc.comv2x

    @property
    def x(self):
        """ Vehicle positions"""
        return self.ego.x


@dataclass
class GlobalGapCoordinator:
    def __init__(self, vehicle_registry: VehicleList):
        self._gclist = [
            VehGapCoordinator(
                veh,
                vehicle_registry.get_leader(veh),
                vehicle_registry.get_follower(veh),
            )
            for veh in vehicle_registry
            if veh.vehtype in DCT_PLT_CONST.get("platoon_types")
        ]
        self._platoons = []
        self.solve_platoons()

    def solve_platoons(self):
        """First iteration to fill the platoon registry based on the current
        vehicle information.
        """

        # This grooups vehicles per road type
        vtf = lambda x: x.ego.link

        # Gap Coord (gc) Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gclist, vtf):
            for gc in group_gc:
                if len(self._platoons) >= 1:
                    newp = PlatoonSet((gc,))
                    tmp = self._platoons[-1] + newp
                    if isinstance(tmp, tuple):
                        self._platoons.append(newp)
                    else:
                        self._platoons[-1] = tmp
                else:
                    self._platoons.append(PlatoonSet((gc,)))
                self._platoons[-1].updatePids()

    def update_platoons(self):
        if len(self._platoons) > 1:
            return
        self.solve_platoons()
