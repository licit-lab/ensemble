"""
Vissim Stream
================
This module is able to receive the stream of data comming from the Vissim platform and define a parser for a specific vehicle data suitable to perform platooning activities. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import Union, Dict, List, Tuple
from collections import defaultdict

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.stream import DataQuery
import ensemble.tools.constants as ct
from ensemble.component.vehiclelist import VehicleList

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

vtypes = Union[float, int, str]
vdata = Tuple[vtypes]
vmaps = Dict[str, vtypes]
vlists = List[vmaps]
response = defaultdict(lambda: False)
simresponse = List[List]


class SimulatorRequest(DataQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize extra things here!

    # =========================================================================
    # MEMORY HANDLING
    # =========================================================================

    @property
    def query(self):
        """String response from the simulator"""
        return self._str_response

    @query.setter
    def query(self, response):
        self._str_response = response
        self.update_vehicle_registry()
        self.dispatch_observers()

    @property
    def current_time(self) -> float:
        "Current simulation second"
        # TODO: How is this updated?
        return self.sim_sec

    @property
    def current_nbveh(self) -> int:
        """Number of vehicles in the network"""
        # TODO: What is self._str_response?
        return len(self._str_response)

    # =========================================================================
    # METHODS
    # =========================================================================

    def create_vehicle_registry(self):
        """Creates a vehicle registry for all vehicles in simulation"""
        self.vehicle_registry = VehicleList(self)

    def update_vehicle_registry(self):
        """Updates vehicle registry in case it exists"""
        if hasattr(self, "vehicle_registry"):
            self.vehicle_registry.update_list()
            return
        self.create_vehicle_registry()

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

        Args:
            response (list): List of list with parameters

        Return:
            listdict (list): List of dictionaries

        """
        if self.query is not None:
            if isinstance(self.query, list):
                return [SimulatorRequest.transform(d) for d in self.query]
            return [SimulatorRequest.transform(self.query)]
        return []

    def is_vehicle_driven(self, vehid: int) -> bool:
        """Returns true if the vehicle state is exposed to a driven state

        Args:
            vehid (str):
                vehicle id

        Returns:
            driven (bool): True if veh is driven
        """
        return False

    @staticmethod
    def transform(veh_data: dict):
        """Transform vehicle data from string format to coherent format

        Args:
            veh_data (dict): vehicle data as received from simulator

        Returns:
            t_veh_data (dict): vehicle data with correct formatting


        Example:
            As an example, for an input of the following style ::

            >>> v = {"CoordFrontX":421.31564190349957
                        "Acceleration":-0.0
                        "Pos":16.25355208592856
                        "No":1,
                        "CoordFrontY":-979.2497097242955
                        "Lane\\Link\\No":6,
                        "VehType":'630',
                        "Speed":83.93049031871615,
                        "Lane\\Index":1,
                    }
            >>> tv = SimulatorRequest.transform(v)
            >>> # Transforms into
            >>> tv == {
            >>>     "abscissa": 421.31564190349957,
            >>>     "acceleration": -0.0,
            >>>     "distance": 16.25355208592856,
            >>>     "driven": False,
            >>>     "elevation": 0.0,
            >>>     "lane": 1,
            >>>     "link": "6",
            >>>     "ordinate": -979.2497097242955,
            >>>     "speed": 23.314025088532265,
            >>>     "vehid": 0,
            >>>     "vehtype": "630",
            >>> },

        """
        for key, val in veh_data.items():
            response[ct.FIELD_DATA_VISSIM[key]] = ct.FIELD_FORMAT_VISSIM[key](
                val
            )
        lkey = "@etat_pilotage"
        response[ct.FIELD_DATA_VISSIM[lkey]] = ct.FIELD_FORMAT_VISSIM[lkey](
            veh_data.get(lkey)
        )
        lkey = "@z"
        response[ct.FIELD_DATA_VISSIM[lkey]] = 0
        return dict(response)
