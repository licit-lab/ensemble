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

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.stream import DataQuery
from symupy.utils.parser import vlists, response
import ensemble.tools.constants as ct

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SimulatorRequest(DataQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._str_response = create_string_buffer(ct.BUFFER_STRING)

    # =========================================================================
    # MEMORY HANDLING
    # =========================================================================

    @property
    def query(self):
        """String response from the simulator"""
        return self._str_response

    @query.setter
    def query(self, response: str):
        self._str_response = response
        for c in self._channels:
            self.dispatch(c)

    @property
    def current_time(self) -> float:
        return float(self.data_query.get("INST").get("@val"))

    @property
    def current_nbveh(self) -> int:
        return int(self.data_query.get("INST").get("@nbVeh"))

    @property
    def data_query(self):
        """Direct parsing from the string buffer

        Returns:
            simdata (OrderedDict): Simulator data parsed from XML
        """
        try:
            dataveh = parse(self._str_response)
            # Transform ordered dictionary into new keys
            return dataveh
        except ExpatError:
            return {}
        except AttributeError:
            return {}

    # =========================================================================
    # METHODS
    # =========================================================================

    def get_vehicle_data(self) -> vlists:
        """Extracts vehicles information from simulators response

        Returns:
            t_veh_data (list): list of dictionaries containing vehicle data with correct formatting

        """
        if self.data_query.get("INST", {}).get("TRAJS") is not None:
            veh_data = self.data_query.get("INST").get("TRAJS")
            if isinstance(veh_data["TRAJ"], list):
                return [SimulatorRequest.transform(d) for d in veh_data["TRAJ"]]
            return [SimulatorRequest.transform(veh_data["TRAJ"])]
        return []

    @staticmethod
    def transform(veh_data: dict):
        """Transform vehicle data from string format to coherent format

        Args:
            veh_data (dict): vehicle data as received from simulator

        Returns:
            t_veh_data (dict): vehicle data with correct formatting


        Example:
            As an example, for an input of the following style ::

            >>> v = OrderedDict([('@abs', '25.00'), ('@acc', '0.00'), ('@dst', '25.00'), ('@id', '0'), ('@ord', '0.00'), ('@tron', 'Zone_001'), ('@type', 'VL'), ('@vit', '25.00'), ('@voie', '1'),('@z', '0')])
            >>> tv = SimulatorRequest.transform(v)
            >>> # Transforms into
            >>> tv == {
            >>>     "abscissa": 25.0,
            >>>     "acceleration": 0.0,
            >>>     "distance": 25.0,
            >>>     "elevation": 0.0,
            >>>     "lane": 1,
            >>>     "link": "Zone_001",
            >>>     "ordinate": 0.0,
            >>>     "speed": 25.0,
            >>>     "vehid": 0,
            >>>     "vehtype": "VL",
            >>> },

        """
        for key, val in veh_data.items():
            response[ct.FIELD_DATA[key]] = ct.FIELD_FORMAT[key](val)
        lkey = "@etat_pilotage"
        response[ct.FIELD_DATA[lkey]] = ct.FIELD_FORMAT[lkey](veh_data.get(lkey))
        return dict(response)

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
