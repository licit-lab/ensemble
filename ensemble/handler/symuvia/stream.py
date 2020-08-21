"""
    This module is able to receive the stream of data comming from the SymuVia platform and define a parser for a specific vehicle data suitable to perform platooning activities. 
"""


""" 
    This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from xmltodict import parse
from xml.parsers.expat import ExpatError

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.stream import DataQuery
from ensemble.component.vehicles import Vehicle, VehicleList

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SimulatorRequest(DataQuery):
    def __init__(self):
        self._strResponse = ""
        self._vehList = []
        self._dctData = {}

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return (
            "Sim Time: {}, VehInNetwork: {}".format(self.current_time, self.current_nbveh)
            if self.parsed_data
            else "No vehicles detected"
        )

    # ============================================================================
    # MEMORY HANDLING
    # ============================================================================

    @property
    def query(self) -> str:
        """
            Parses response from simulator to data
        """
        return self._strResponse.value

    @query.setter
    def query(self, response: str = None) -> None:
        """
            Parses response from simulator to data
        """

        # 1. gets string
        self._strResponse = response

        # 2. parses data
        try:
            self._dctData = parse(self._strResponse.value)
        except ExpatError:
            self._dctData = {}

        # 3. vehicle list
        self.update_vehicle_list()

    @property
    def parsed_data(self) -> dict:
        """ 
            Returns current data dictionary
        """
        return self._dctData

    @property
    def vehicles(self):
        return self._vehList.vehicles

    @property
    def current_time(self) -> str:
        return self.parsed_data.get("INST").get("@val")

    @property
    def current_nbveh(self) -> int:
        return self.parsed_data.get("INST").get("@nbVeh")

    # ============================================================================
    # METHODS
    # ============================================================================

    def update_vehicle_list(self):
        """ 
            Construct and or update vehicle data
        """
        if self._vehList:
            self._vehList.update_list(self.get_vehicle_data())
            return
        self._vehList = VehicleList.from_request(self.get_vehicle_data())

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

        :param response: Simulator response
        :type response: str
        :return: list of vehicles in the network
        :rtype: list of dictionaries
        """
        if self.parsed_data.get("INST", {}).get("TRAJS") is not None:
            veh_data = self.parsed_data.get("INST").get("TRAJS")
            if isinstance(veh_data["TRAJ"], list):
                return veh_data["TRAJ"]
            return [veh_data["TRAJ"]]
        return []

    def get_vehicle_id(self) -> tuple:
        """Extracts vehicle ids information from simulators response

        :return: tuple containing vehicle ids at current state in all network
        :rtype: list
        """
        return tuple(veh.get("@id") for veh in self.get_vehicle_data())

    def query_vehicle_link(self, vehid: str, *args) -> tuple:
        """ Extracts current vehicle link information from simulators response

        :param vehid: vehicle id multiple arguments accepted
        :type vehid: str
        :return: vehicle link in tuple form
        :rtype: tuple
        """
        vehids = set((vehid, *args)) if args else vehid
        vehid_pos = self.query_vehicle_data_dict("@tron", vehids)
        return tuple(vehid_pos.get(veh) for veh in vehids)

    def query_vehicle_position(self, vehid: str, *args) -> tuple:
        """ Extracts current vehicle distance information from simulators response

        :param vehid: vehicle id multiple arguments accepted
        :type vehid: str
        :return: vehicle distance in link in tuple form
        :rtype: tuple
        """
        vehids = set((vehid, *args)) if args else vehid
        vehid_pos = self.query_vehicle_data_dict("@dst", vehids)
        return tuple(vehid_pos.get(veh) for veh in vehids)

    def query_vehicle_data_dict(self, dataval: str, vehid: str, *args) -> dict:
        """ Extracts and filters vehicle data from the simulators response

        :param dataval: parameter to be extracted e.g. '@id', '@dst'
        :type dataval: str
        :param vehid: vehicle id, multiple arguments accepted
        :type vehid: str
        :return: dictionary where key is @id and value is dataval
        :rtype: dict
        """
        vehids = set((vehid, *args)) if args else set(vehid)
        data_vehs = [(veh.get("@id"), veh.get(dataval)) for veh in self.get_vehicle_data() if veh.get("@id") in vehids]
        return dict(data_vehs)

    def is_vehicle_in_network(self, vehid: str, *args) -> bool:
        """True if veh id is in the network at current state, for multiple arguments
           True if all veh ids are in the network

        :param vehid: Integer of vehicle id, comma separated if testing for multiple
        :type vehid: int
        :return: True if vehicle is in the network otherwise false
        :rtype: bool
        """
        all_vehs = self.get_vehicle_id()
        if not args:
            return vehid in all_vehs
        vehids = set((vehid, *args))
        return set(vehids).issubset(set(all_vehs))

    def vehicle_in_link(self, link: str, lane: str = "1") -> tuple:
        """Returns a tuple containing vehicle ids traveling on the same link+lane at current state

        :param link: link name
        :type link: str
        :param lane: lane number, defaults to '1'
        :type lane: str, optional
        :return: tuple containing vehicle ids
        :rtype: tuple
        """
        return tuple(
            veh.get("@id") for veh in self.get_vehicle_data() if veh.get("@tron") == link and veh.get("@voie") == lane
        )

    def is_vehicle_in_link(self, veh: str, link: str) -> bool:
        """ Returns true if a vehicle is in a link at current state
        
        :param veh: vehicle id
        :type veh: str
        :param link: link name
        :type link: str
        :return: True if veh is in link
        :rtype: bool
        """
        veh_ids = self.vehicle_in_link(link)
        return set(veh).issubset(set(veh_ids))

    def vehicle_downstream_of(self, vehid: str) -> tuple:
        """Get ids of vehicles downstream to vehid

        :param vehid: integer describing id of reference veh
        :type vehid: int
        :return: tuple with ids of vehicles ahead (downstream)
        :rtype: tuple
        """
        link = self.query_vehicle_link(vehid)[0]
        vehpos = self.query_vehicle_position(vehid)[0]

        vehids = set(self.vehicle_in_link(link))
        neigh = vehids.difference(set(vehid))

        neighpos = self.query_vehicle_position(*neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if float(npos) > float(vehpos))

    def vehicle_upstream_of(self, vehid: str) -> tuple:
        """Get ids of vehicles upstream to vehid

        :param vehid: integer describing id of reference veh
        :type vehid: int
        :return: tuple with ids of vehicles behind (upstream)
        :rtype: tuple
        """
        link = self.query_vehicle_link(vehid)[0]
        vehpos = self.query_vehicle_position(vehid)[0]

        vehids = set(self.vehicle_in_link(link))
        neigh = vehids.difference(set(vehid))

        neighpos = self.query_vehicle_position(*neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if float(npos) < float(vehpos))

    def __contains__(self, elem: Vehicle) -> bool:
        return elem in self._vehList