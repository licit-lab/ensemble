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

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

vtypes = Union[float, int, str]
vdata = Tuple[vtypes]
vmaps = Dict[str, vtypes]
vlists = List[vmaps]
response = defaultdict(lambda: False)
vissim_response = List[List]


class SimulatorRequest(DataQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize extra things here!

    @property
    def current_time(self) -> float:
        "Current simulation second"
        # TODO: How is this updated?
        return self.sim_sec

    @property
    def current_nbveh(self) -> int:
        """ Number of vehicles in the network"""
        # TODO: What is self._str_response?
        return len(self._str_response)

    @property
    def query(self):
        """String response from the simulator"""
        return self._str_response

    @query.setter
    def query(self, response: vissim_response):
        self._str_response = response
        for c in self._channels:
            self.dispatch(c)

    def is_vehicle_driven(self, vehid: int) -> bool:
        """Returns true if the vehicle state is exposed to a driven state

        Args:
            vehid (str):
                vehicle id

        Returns:
            driven (bool): True if veh is driven
        """
        # if self.is_vehicle_in_network(vehid):

        #     forced = tuple(
        #         veh.get("driven") == True
        #         for veh in self.get_vehicle_data()
        #         if veh.get("vehid") == vehid
        #     )
        #     return any(forced)
        # return False
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

    # def get_leader_id(self, vehid):
    #     try:
    #         downstream_ids = tuple(self.vehicle_downstream_of(vehid))
    #         dict_pos = self.query_vehicle_data_dict("Pos", *downstream_ids)
    #         leader_id = min(dict_pos, key=dict_pos.get)
    #     except IndexError:
    #         leader_id = -1
    #     except TypeError:
    #         leader_id = -1
    #     return leader_id

    # def get_follower_id(self, vehid):
    #     try:
    #         upstream_ids = tuple(self.vehicle_upstream_of(vehid))
    #         dict_pos = self.query_vehicle_data_dict("Pos", *upstream_ids)
    #         follower_id = max(dict_pos, key=dict_pos.get)
    #     except IndexError:
    #         follower_id = -1
    #     except TypeError:
    #         follower_id = -1
    #     return follower_id
