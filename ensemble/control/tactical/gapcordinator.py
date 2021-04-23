"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pandas as pd
import networkx as nx
from itertools import groupby
from dataclasses import dataclass, asdict


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehiclelist import VehicleList
from ensemble.logic.platoon_set import PlatoonSet
from ensemble.logic.subscriber import Subscriber
from ensemble.control.tactical.vehcoordinator import (
    VehGapCoordinator,
    MAXNDST,
    PLT_TYP,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


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
            if veh.vehtype in PLT_TYP:
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
                self._gcnet.nodes()[veh.vehid].get(
                    "vgc"
                ).leader = self._gcnet.nodes()[leader.vehid].get("vgc")

    def _update_states(self):
        """ Update platoon state according to current information"""

        # Gap Coord (gc) Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gcnet.nodes(data=True), vtf):
            for _, gc in group_gc:
                gc.get("vgc").status = gc.get("vgc").solve_state()

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
        for _, vgc in self._gcnet.nodes(data=True):
            data = vgc.get("vgc")
            d = asdict(data)
            d = dict(d, **asdict(data.ego))
            d["platoonid"] = data.platoonid
            veh_data.append(d)
        df = pd.DataFrame(veh_data)
        return df.set_index(["platoonid", "vehid"]) if not df.empty else df

    def __str__(self):
        if self._gcnet is None:
            return "No vehicles have been registered"
        return str(self._to_pandas())

    def __repr__(self):
        if self._gcnet is None:
            return "No vehicles have been registered"
        return repr(self._to_pandas())

    def update_platoons(self):
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