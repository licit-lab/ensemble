"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

import pandas as pd
import numpy as np
import networkx as nx
from itertools import groupby

from dataclasses import dataclass, asdict

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
from ensemble.logic.subscriber import Subscriber
from ensemble.tools.constants import DCT_PLT_CONST
from ensemble.metaclass.coordinator import AbsSingleGapCoord

PLState = Union[StandAlone, Platooning, Joining, Splitting]

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

MAXTRKS = DCT_PLT_CONST["max_platoon_length"]
MAXNDST = DCT_PLT_CONST["max_connection_distance"]
PLT_TYP = DCT_PLT_CONST["platoon_types"]


@dataclass
class FrontGap:
    def __init__(self, vehicle: AbsSingleGapCoord = None):
        self.vgc = vehicle


@dataclass
class RearGap:
    def __init__(self, vehicle: AbsSingleGapCoord = None):
        self.vgc = vehicle


@dataclass
class VehGapCoordinator(AbsSingleGapCoord):

    status: PLState = StandAlone()
    platoon: bool = False
    comv2x: bool = True

    def __init__(self, vehicle: Vehicle):
        self.ego = vehicle
        self._fgc = None
        self._rgc = None
        self.pid = 0
        # self.solve_fgc_state()

    def __hash__(self):
        return hash((type(self), self.ego.vehid))

    def set_leader(self, leader: AbsSingleGapCoord):
        self._fgc = leader

    def solve_fgc_state(self):
        """Logic solver for the platoon state machine."""
        if self._fgc is not None:
            self._fgc.status.next_state(self)

    @property
    def x(self):
        """ Ego current position in link """
        return self.ego.distance

    @property
    def leader(self):
        """ Returns the leader vehicle in the platoon"""
        return self._fgc if self._fgc is not None else self.ego

    @property
    def follower(self):
        """ Returns the follower vehicle in the platoon"""
        return self._rgc if self._rgc is not None else self.ego

    @property
    def is_head(self):
        """ Determines if the vehicle is head of the platoon"""
        return self.leader is self.ego

    @property
    def is_tail(self):
        """ Determines if the vehicle is tail of the platoon """
        return self.follower is self.ego

    @property
    def ttd(self):
        """ Total travel time"""
        return self.ego.ttd

    @property
    def vehid(self):
        """ Vehicle positions"""
        return self.ego.vehid

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
        return (
            (self.pid < MAXTRKS - 1)
            and (self.dx < MAXNDST)
            and self._fgc.comv2x
        )

    def cancel_join_request(self, value: bool = False):
        return not self.joinable and value


# This grooups vehicles per road type
vtf = lambda x: x[1].get("vgc").ego.link


@dataclass
class GlobalGapCoordinator(Subscriber):
    def __init__(self, vehicle_registry: VehicleList):
        self._gcnet = nx.DiGraph()
        super().__init__(vehicle_registry)
        self._platoons = []
        self._add_vehicle_gc()
        self.solve_platoons()

    def _add_vehicle_gc(self):
        # Add all vehicles gap coord
        for veh in self._publisher:
            if veh.vehtype in DCT_PLT_CONST.get("platoon_types"):
                self._gcnet.add_node(veh.vehid, vgc=VehGapCoordinator(veh))
        self._set_leaders(self._publisher)

    def _set_leaders(self, vehicle_registry: VehicleList):
        """ Set initial leaders for the formation"""

        for veh in vehicle_registry:
            leader = vehicle_registry.get_leader(veh, distance=MAXNDST)
            if (
                leader is not None
                and leader.vehtype in PLT_TYP
                and veh.vehtype in PLT_TYP
            ):
                self._gcnet.add_edge(veh.vehid, leader.vehid)
                self._gcnet.nodes()[veh.vehid].get("vgc").set_leader(
                    self._gcnet.nodes()[leader.vehid].get("vgc")
                )

    def _update_states(self):
        """ Update platoon state according to current information"""

        # Add new vehicle gap coordinators
        self._add_vehicle_gc()

        # Gap Coord (gc) Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gcnet.nodes(data=True), vtf):
            for _, gc in group_gc:
                gc.get("vgc").solve_fgc_state()

    def __hash__(self):
        return hash(self._publisher)

    def __getitem__(self, index):
        result = self._gcnet.nodes()[index].get("vgc")
        return result

    def _to_pandas(self) -> pd.DataFrame:
        """Transforms vehicle list into a pandas for rendering purposes

        Returns:
            df (DataFrame): Returns a table with pandas data.

        """
        veh_data = []
        for i, vgc in self._gcnet.nodes(data=True):
            data = vgc.get("vgc")
            d = asdict(data)
            d = dict(d, **asdict(data.ego))
            d["pid"] = data.pid
            veh_data.append(d)
        df = pd.DataFrame(veh_data)
        return df.set_index(["pid", "vehid"]) if not df.empty else df

    def __str__(self):
        if self._gcnet is None:
            return "No vehicles have been registered"
        return str(self._to_pandas())

    def __repr__(self):
        if self._gcnet is None:
            return "No vehicles have been registered"
        return repr(self._to_pandas())

    def solve_platoons(self):
        """First iteration to fill the platoon registry based on the current
        vehicle information.
        """

        # Add new vehicle gap coordinators
        self._add_vehicle_gc()

        # Gap Coord (gc) Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gcnet.nodes(data=True), vtf):
            for _, gc in group_gc:
                if len(self._platoons) >= 1:
                    newp = PlatoonSet((gc.get("vgc"),))
                    tmp = self._platoons[-1] + newp
                    if isinstance(tmp, tuple):
                        self._platoons.append(newp)
                    else:
                        self._platoons[-1] = tmp
                else:
                    self._platoons.append(PlatoonSet((gc.get("vgc"),)))
                self._platoons[-1].updatePids()

        self._update_states()

    def update_platoons(self):
        self.solve_platoons()
