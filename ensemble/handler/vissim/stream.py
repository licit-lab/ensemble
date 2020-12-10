"""
Vissim Stream
================
This module is able to receive the stream of data comming from the Vissim platform and define a parser for a specific vehicle data suitable to perform platooning activities. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import List
from symupy.components import Vehicle, VehicleList

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.stream import DataQuery

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

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
        """ Returns true if the vehicle state is exposed to a driven state

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

    def get_vehicle_data(self) -> list:
        """ Extracts vehicles information from simulators response

            Args:
                response (list): List of list with parameters 
            
            Return: 
                listdict (list): List of dictionaries 
        
        """
        vehsAttributesNames = (
            "abscissa",
            "acceleration",
            "distance",
            "vehid",
            "ordinate",
            "link",
            "vehtype",
            "speed",
            "lane",
        )
        listofdict = [
            dict(zip(vehsAttributesNames, item)) for item in self.query
        ]
        # veh_list = VehicleList.from_request(listofdict)
        return listofdict

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
