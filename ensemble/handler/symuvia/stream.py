"""
SymuVia Stream
================
This module is able to receive the stream of data comming from the SymuVia platform and define a parser for a specific vehicle data suitable to perform platooning activities. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from xmltodict import parse
from xml.parsers.expat import ExpatError
from ctypes import create_string_buffer
from typing import Union, Dict, List, Tuple
from collections import defaultdict

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.stream import DataQuery
import ensemble.tools.constants as ct
from ensemble.handler.symuvia.xmlparser import XMLTrajectory
from ensemble.component.vehiclelist import VehicleList

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

vtypes = Union[float, int, str]
vdata = Tuple[vtypes]
vmaps = Dict[str, vtypes]
vlists = List[vmaps]
response = defaultdict(lambda: False)


class SimulatorRequest(DataQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datatraj = XMLTrajectory(b"")

    # =========================================================================
    # MEMORY HANDLING
    # =========================================================================

    @property
    def query(self):
        """String response from the simulator"""
        return self.datatraj._xml

    @query.setter
    def query(self, response: bytes):
        self.datatraj = XMLTrajectory(response)
        self.update_vehicle_registry()
        self.dispatch()

    @property
    def current_time(self) -> float:
        return self.datatraj.inst

    @property
    def current_nbveh(self) -> int:
        return self.datatraj.nbveh

    @property
    def data_query(self):
        """Direct parsing from the string buffer

        Returns:
            simdata (OrderedDict): Simulator data parsed from XML
        """

        return self.datatraj.todict

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

    def get_vehicle_data(self) -> tuple:
        """Extracts vehicles information from simulators response

        Returns:
            t_veh_data (list): list of dictionaries containing vehicle data with correct formatting

        """
        return self.data_query

    def is_vehicle_driven(self, vehid: int) -> bool:
        """Returns true if the vehicle state is exposed to a driven state

        Args:
            vehid (str):
                vehicle id

        Returns:
            driven (bool): True if veh is driven
        """
        if self.is_vehicle_in_network(vehid):

            forced = tuple(
                veh.get("driven") == True
                for veh in self.get_vehicle_data()
                if veh.get("vehid") == vehid
            )
            return any(forced)
        return False
