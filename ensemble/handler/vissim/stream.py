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

    # NOTE: This is from symuvia
    # @property
    # def query(self):
    #     """String response from the simulator"""
    #     return self._str_response

    # @query.setter
    # def query(self, response: str):
    #     self._str_response = response
    #     for c in self._channels:
    #         self.dispatch(c)

    # def is_vehicle_driven(self, vehid: int) -> bool:
    #     """ Returns true if the vehicle state is exposed to a driven state

    #         Args:
    #             vehid (str):
    #                 vehicle id

    #         Returns:
    #             driven (bool): True if veh is driven
    #     """
    #     if self.is_vehicle_in_network(vehid):

    #         forced = tuple(
    #             veh.get("driven") == True
    #             for veh in self.get_vehicle_data()
    #             if veh.get("vehid") == vehid
    #         )
    #         return any(forced)
    #     return False

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

            :param response: Simulator response
            :type response: str
            :return: list of vehicles in the network
            :rtype: list of dictionaries
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
        vehsAttributes = self._str_response
        listofdict = [
            dict(zip(vehsAttributesNames, item)) for item in vehsAttributes
        ]
        # veh_list = VehicleList.from_request(listofdict)
        return listofdict

    # def parse_data(self, response: List = None, simsec: float = 0) -> List:
    #     """Parses response from simulator to data

    #     :param response: Simulator response
    #     :type response: str
    #     :return: Full simulator response
    #     :rtype: dict
    #     """
    #     self.sim_sec = simsec
    #     self._str_response = response

    # def get_vehicle_data_vissim(self) -> list:
    #     """Extracts vehicles information from simulators response

    #     :param response: Simulator response
    #     :type response: str
    #     :return: list of vehicles in the network
    #     :rtype: list of dictionaries
    #     """
    #     vehsAttributesNames = (
    #         "abscissa",
    #         "acceleration",
    #         "distance",
    #         "vehid",
    #         "ordinate",
    #         "link",
    #         "vehtype",
    #         "speed",
    #         "lane",
    #     )
    #     vehsAttributesNamesVissim = (
    #         "CoordFrontX",
    #         "Acceleration",
    #         "Pos",
    #         "No",
    #         "CoordFrontY",
    #         "Lane\\Link\\No",
    #         "VehType",
    #         "Speed",
    #         "Lane\\Index",
    #     )
    #     vehsAttributes = self._str_response
    #     return [
    #         dict(zip(vehsAttributesNamesVissim, item))
    #         for item in vehsAttributes
    #     ]

    # def get_vehicle_id(self) -> tuple:
    #     """Extracts vehicle ids information from simulators response

    #     :return: tuple containing vehicle ids at current state in all network
    #     :rtype: list
    #     """
    #     return tuple(veh.get("No") for veh in self.get_vehicle_data_vissim())

    # def query_vehicle_link(self, vehid: int, *args) -> tuple:
    #     """ Extracts current vehicle link information from simulators response

    #     :param vehid: vehicle id multiple arguments accepted
    #     :type vehid: str
    #     :return: vehicle link in tuple form
    #     :rtype: tuple
    #     """
    #     vehids = set((vehid, *args)) if args else vehid
    #     vehid_pos = self.query_vehicle_data_dict("Lane\\Link\\No", vehids)
    #     if type(vehids) == set:
    #         links = tuple(vehid_pos.get(veh) for veh in vehids)
    #     else:
    #         links = tuple([vehid_pos.get(vehid)])
    #     return links

    # def query_vehicle_position(self, vehid: int, *args) -> tuple:
    #     """ Extracts current vehicle distance information from simulators response

    #     :param vehid: vehicle id multiple arguments accepted
    #     :type vehid: str
    #     :return: vehicle distance in link in tuple form
    #     :rtype: tuple
    #     """
    #     vehids = set((vehid, *args)) if args else vehid
    #     vehid_pos = self.query_vehicle_data_dict("Pos", vehids)
    #     if type(vehids) == set:
    #         positions = tuple(vehid_pos.get(veh) for veh in vehids)
    #     else:
    #         positions = tuple([vehid_pos.get(vehid)])
    #     return positions

    # def query_vehicle_data_dict(self, dataval: str, vehid: int, *args) -> dict:
    #     """ Extracts and filters vehicle data from the simulators response

    #     :param dataval: parameter to be extracted e.g. '@id', '@dst'
    #     :type dataval: str
    #     :param vehid: vehicle id, multiple arguments accepted
    #     :type vehid: str
    #     :return: dictionary where key is @id and value is dataval
    #     :rtype: dict
    #     """
    #     vehids = set((vehid, *args)) if args else vehid

    #     if type(vehids) == set:
    #         data_vehs = [
    #             (veh.get("No"), veh.get(dataval))
    #             for veh in self.get_vehicle_data_vissim()
    #             if veh.get("No") in vehids
    #         ]
    #     else:
    #         data_vehs = [
    #             (veh.get("No"), veh.get(dataval))
    #             for veh in self.get_vehicle_data_vissim()
    #             if veh.get("No") == vehids
    #         ]
    #     return dict(data_vehs)

    # def is_vehicle_in_network(self, vehid: int, *args) -> bool:
    #     """True if veh id is in the network at current state, for multiple arguments
    #        True if all veh ids are in the network

    #     :param vehid: Integer of vehicle id, comma separated if testing for multiple
    #     :type vehid: int
    #     :return: True if vehicle is in the network otherwise false
    #     :rtype: bool
    #     """
    #     all_vehs = self.get_vehicle_id()
    #     if not args:
    #         return vehid in all_vehs
    #     vehids = set((vehid, *args))
    #     return set(vehids).issubset(set(all_vehs))

    # def vehicle_in_link(self, link: int, lane: int = 1) -> tuple:
    #     """Returns a tuple containing vehicle ids traveling on the same link+lane at current state

    #     :param link: link name
    #     :type link: int
    #     :param lane: lane number, defaults to 1
    #     :type lane: int, optional
    #     :return: tuple containing vehicle ids
    #     :rtype: tuple
    #     """
    #     return tuple(
    #         veh.get("No")
    #         for veh in self.get_vehicle_data_vissim()
    #         if veh.get("Lane\\Link\\No") == link
    #         and veh.get("Lane\\Index") == lane
    #     )

    # def is_vehicle_in_link(self, veh: int, link: int) -> bool:
    #     """ Returns true if a vehicle is in a link at current state

    #     :param veh: vehicle id
    #     :type veh: int
    #     :param link: link name
    #     :type link: int
    #     :return: True if veh is in link
    #     :rtype: bool
    #     """
    #     veh_ids = self.vehicle_in_link(link)
    #     return set(veh).issubset(set(veh_ids))

    # def vehicle_downstream_of(self, vehid: int) -> tuple:
    #     """Get ids of vehicles downstream to vehid

    #     :param vehid: integer describing id of reference veh
    #     :type vehid: int
    #     :return: tuple with ids of vehicles ahead (downstream)
    #     :rtype: tuple
    #     """
    #     link = self.query_vehicle_link(vehid)[0]
    #     vehpos = self.query_vehicle_position(vehid)[0]

    #     vehids = set(self.vehicle_in_link(link))
    #     neigh = vehids.difference({vehid})

    #     neighpos = self.query_vehicle_position(*neigh)

    #     return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos > vehpos)

    # def vehicle_upstream_of(self, vehid: int) -> tuple:
    #     """Get ids of vehicles upstream to vehid

    #     :param vehid: integer describing id of reference veh
    #     :type vehid: int
    #     :return: tuple with ids of vehicles behind (upstream)
    #     :rtype: tuple
    #     """
    #     link = self.query_vehicle_link(vehid)[0]
    #     vehpos = self.query_vehicle_position(vehid)[0]

    #     vehids = set(self.vehicle_in_link(link))
    #     neigh = vehids.difference({vehid})

    #     neighpos = self.query_vehicle_position(*neigh)

    #     return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos < vehpos)

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

    # def dispatch(self, channel: str) -> None:
    #     """ This is a dispatcher for the vehicle

    #     :param channel: Channel to broadcast to (FGC/RGC/ALL)
    #     :type vehid: str

    #     """

    #     for subscriber, callback in self.get_subscribers(channel).items():
    #         vehicle_env = {}
    #         callback(vehicle_env)

    # def create_vehicle_list(self):
    #     """Initialize
    #     """
    #     if not self._vehs:
    #         self._vehs = VehicleList.from_request(self.get_vehicle_data())
    #         return

    # def update_vehicle_list(self):
    #     """ Construct and or update vehicle data
    #     """
    #     if self._vehs:
    #         self._vehs.update_list(self.get_vehicle_data())
    #         return
    #     self.create_vehicle_list()

    # def __contains__(self, elem: Vehicle) -> bool:
    #     return elem in self._vehs

    # @property
    # def vehicles(self):
    #     self.update_vehicle_list()
    #     return self._vehs
