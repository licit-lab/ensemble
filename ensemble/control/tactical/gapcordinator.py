"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import Iterable
import pandas as pd
import networkx as nx
from itertools import groupby
from dataclasses import dataclass, asdict
from itertools import chain


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehiclelist import EMPTY_MESSAGE, VehicleList
from ensemble.logic.platoon_set import PlatoonSet
from ensemble.logic.subscriber import Subscriber
from ensemble.control.tactical.vehcoordinator import (
    VehGapCoordinator,
    MAXNDST,
    PLT_TYP,
)
from ensemble.metaclass.controller import AbsController
from ensemble.tools.screen import log_in_terminal

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

EMPTY_MESSAGE = "\tNo platoons have been registered"


@dataclass
class GlobalGapCoordinator(Subscriber):
    def __init__(self, vehicle_registry: VehicleList):
        self._gcnet = nx.DiGraph()
        super().__init__(vehicle_registry)
        self.platoon_sets = {}
        self.free_gcs = []
        self.update_platoons()

    # =========================================================================
    # PROTOCOLS
    # =========================================================================
    def __hash__(self):
        return hash(self._publisher)

    def __getitem__(self, index):
        result = self._gcnet.nodes()[index].get("vgc")
        return result

    def pandas_print(self, columns: Iterable = []) -> pd.DataFrame:
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
            d["distance"] = data.ego.distance
            veh_data.append(d)
        df = pd.DataFrame(veh_data)
        if columns and not df.empty:
            df = df[columns]
        return df.set_index(["platoonid", "vehid"]) if not df.empty else df

    def pretty_print(self, columns: list = []) -> str:
        """Summary of info"""
        df = self.pandas_print(["platoonid", "vehid"] + columns)
        return EMPTY_MESSAGE if df.empty else str(df)

    def __str__(self):
        if self._gcnet is None:
            return EMPTY_MESSAGE
        return str(self.pandas_print())

    def __repr__(self):
        if self._gcnet is None:
            return EMPTY_MESSAGE
        return repr(self.pandas_print())

    def __len__(self):
        if self._gcnet is None:
            return 0
        return len(self._gcnet.nodes)

    # =========================================================================
    # METHODS
    # =========================================================================

    def update(self):
        """Follower method to add/release vehicle gapcoordinator"""

        self.add_vehicle_gcs()
        self.release_vehicle_gcs()
        self.update_leaders()

    def add_vehicle_gcs(self):
        """Add all gap coordinators w.r.t publisher"""
        for veh, _ in self._publisher.iterate_links_distances():
            vgc = VehGapCoordinator(veh)
            self.add_gapcoordinator(vgc)

    def release_vehicle_gcs(self):
        """Releases all gap coordinators w.r.t publihser"""
        for vgc in self.iter_group_link(downtoup=True, group=True):
            if (
                vgc.ego.vehid
                # not in self._publisher._request.get_vehicles_property("vehid")
                not in [v.vehid for v in self._publisher]
            ):
                self.release_gapcoordinator(vgc)

    def vgcs(self):
        "Existing vehicle gap coordinators"
        return iter(
            map(lambda x: x[1].get("vgc"), self._gcnet.nodes(data=True))
        )

    def add_gapcoordinator(self, vgc: VehGapCoordinator):
        """Adds a single gap coordinator to the list"""
        if vgc not in self.vgcs() and vgc.ego.vehtype in PLT_TYP:
            self._gcnet.add_node(vgc.ego.vehid, vgc=vgc)
            self[vgc.ego.vehid].init_reference()
            self.update_leader(vgc)

    def release_gapcoordinator(self, vgc: VehGapCoordinator):
        """Releases a single gap coordinator from the node list"""
        self._gcnet.remove_node(vgc.ego.vehid)
        self.free_gcs.append(vgc)

    def update_leader(self, vgc: VehGapCoordinator):
        """Add or creates leader for a specific gap coordinator"""
        leader = self._publisher.get_leader(vgc.ego, distance=MAXNDST)
        if (
            leader is not None
            and leader.vehtype in PLT_TYP
            and vgc.ego.vehtype in PLT_TYP
        ):
            self._gcnet.add_edge(vgc.ego.vehid, leader.vehid)
            self[vgc.ego.vehid].leader = self[leader.vehid]
            self[vgc.ego.vehid].leader_data = {"id": leader.vehid}

    def update_leaders(self):
        """Updates leaders for all gap coordinators"""
        for vgc in self.iter_group_link(downtoup=True, group=True):
            self.update_leader(vgc)

    def update_states(self):
        """Update platoon state according to current information"""
        for vgc in self.iter_group_link(downtoup=True, group=True):
            vgc.status = vgc.solve_state()

    def iter_group_link(self, downtoup=True, group=False):
        """Iteratorator by link ordered from largest ttd towards smaller

        Args:
            downtoup (bool, optional): Downstream to upstream. Defaults to True.
            group (bool, optional): Returns without grouping per platoon. Defaults to False.

        Yields:
            vgc (VehicleGapCoordinator): Vehicle gap coordinator or iterable.
        """
        vtf = lambda x: x[1].get("vgc").ego.link
        vgcs = sorted(
            self._gcnet.nodes(data=True),
            key=lambda x: x[1].get("vgc").ego.ttd,
            reverse=downtoup,
        )
        for _, group_gc in groupby(vgcs, vtf):
            if group:
                for _, gc in group_gc:
                    yield gc.get("vgc")
            else:
                yield group_gc

    def create_platoon_sets(self):
        """Create all platoons subsets"""
        converter = lambda x: x[1].get("vgc")
        for vgc in self.iter_group_link(downtoup=True, group=True):
            if not vgc.platoon:
                if vgc.leader.ego == vgc.ego or vgc.ego in PLT_TYP:
                    # Head
                    ps = PlatoonSet((vgc,))
                    self.platoon_sets[ps.platoonid] = ps
                    vgc.positionid = len(ps) - 1
                else:
                    # Try join from behind

                    # Retrieve id of leader
                    lps = self.platoon_sets[vgc.leader.platoonid]
                    nwps = PlatoonSet((vgc,))
                    jps = lps + nwps

                    if isinstance(jps, tuple):
                        # This means back was refused
                        self.platoon_sets[jps[1].platoonid] = jps[1]
                        vgc.positionid = len(jps[1]) - 1
                    else:
                        self.platoon_sets[vgc.leader.platoonid] = jps
                        PlatoonSet.set_pid(
                            nwps.platoonid
                        )  # Retrieves former id
                        vgc.positionid = len(jps) - 1
                vgc.platoon = True

    def update_platoons(self):
        """First iteration to fill the platoon registry based on the current
        vehicle information.
        """

        # The main idea to update the  platoon_registry is the following:
        # 1. Once the vehicle registry is updated, via a dispatch may update
        #    the list of gap coordinators.
        # 2. When entering here gap coordinators should be available.
        # 3. W
        # 2. Merge gap coordinators:
        #    2a. Iterate over gc per link
        #    2b. Iterate from upstream towards downstream on gc (small with largest ttd)
        #    2c. Consider the gc on the current link
        #    2d. For ech gc find it's leader.
        #        2d1. Create a platoon set for the vehicle with less ttd
        #        2d1. Is my leader joinable?
        #             yes -> join current platoon set with my leader
        #             no -> return

        self.update()

        # Gap Coord (gc) Group by link (Vehicle in same link)
        self.create_platoon_sets()

        self.update_states()

    @property
    def nplatoons(self) -> int:
        """Return the number of created platoons"""
        return len(self.platoon_sets.keys())

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

        for vgc in self.iter_group_link(downtoup=True, group=True):
            vgc.evolve_control(self.cacc, time)
