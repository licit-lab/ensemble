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
from ensemble.metaclass.controller import AbsController

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
        self.update_platoons()

    def _add_vehicle_gc(self):
        # Add all vehicles gap coord
        for veh in self._publisher:
            if veh.vehtype in PLT_TYP:
                self._gcnet.add_node(veh.vehid, vgc=VehGapCoordinator(veh))
                self[veh.vehid].init_reference()
        self._set_leaders(self._publisher)

    def _set_leaders(self, vehicle_registry: VehicleList):
        """Set initial leaders for the formation"""

        for veh in vehicle_registry:
            leader = vehicle_registry.get_leader(veh, distance=MAXNDST)
            if (
                leader is not None
                and leader.vehtype in PLT_TYP
                and veh.vehtype in PLT_TYP
            ):
                self._gcnet.add_edge(veh.vehid, leader.vehid)
                self[veh.vehid].leader = self[leader.vehid]
                self[veh.vehid].leader_data = {"id": leader.vehid}

    def _update_states(self):
        """Update platoon state according to current information"""

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

    def __len__(self):
        if self._gcnet is None:
            return 0
        return len(self._gcnet.nodes)

    def update_platoons(self):
        """First iteration to fill the platoon registry based on the current
        vehicle information.
        """

        # Add new vehicle gap coordinators
        self._add_vehicle_gc()

        # Gap Coord (gc) Group by link (Vehicle in same link)
        for _, group_gc in groupby(self._gcnet.nodes(data=True), vtf):
            for _, gc in group_gc:
                vgc = gc.get("vgc")
                newplatoon = PlatoonSet((vgc,))
                if len(self._platoons) >= 1:
                    tmp = self._platoons[-1] + newplatoon
                    if isinstance(tmp, tuple):
                        self._platoons.append(newplatoon)
                    else:
                        self._platoons[-1] = tmp
                else:
                    self._platoons.append(newplatoon)
                self._platoons[-1].updatePids()

        self._update_states()

    @property
    def cacc(self):
        """Returns the operational controller object"""
        return self._cacc

    @cacc.setter
    def cacc(self, control: AbsController):
        """A function just to attach the control of the system to the layer and initialize the references

        Args:
            control (AbsController): Callable, operational controller
        """
        self._cacc = control

    def apply_cacc(self, time: float):
        """This method intends to apply the cacc over all vehicles within the platoon at specific time step"""

        for _, group_gc in groupby(self._gcnet.nodes(data=True), vtf):
            for _, gc in group_gc:
                vcg = gc.get("vgc")
                vcg.evolve_control(self.cacc, time)
