"""
    This module is able to receive the stream of data comming from the SymuVia platform and define a parser for a specific vehicle data suitable to perform platooning activities. 
"""


""" 
    This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

#from xmltodict import parse
#from xml.parsers.expat import ExpatError
from typing import List
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
        self._str_response = ""
        self._vehs = []

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return (
            "Sim Time: {}, VehInNetwork: {}".format(self.current_time, self.current_nbveh)
            if self.data_query
            else "Simulation has not started"
        )

    def parse_data(self, response: List = None) -> List:
        """Parses response from simulator to data

        :param response: Simulator response
        :type response: str
        :return: Full simulator response
        :rtype: dict
        """
        self._str_response = response

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

        :param response: Simulator response
        :type response: str
        :return: list of vehicles in the network
        :rtype: list of dictionaries
        """
        vehsAttributesNames=('abscisa','acceleration', 'distance','vehid','ordinate','link','vehtype','speed','lane')
        vehsAttributesNamesVissim = ('CoordFrontX', 'Acceleration', 'Pos', 'No', 'CoordFrontY', 'Lane\\Link\\No', 'VehType', 'Speed', 'Lane\\Index')
        vehsAttributes =self._str_response
        print('Current Number of vehicles in the network  is ',len(vehsAttributes))


        listofdict=[dict(zip(vehsAttributesNames, item)) for item in vehsAttributes]
        veh_list = VehicleList.from_request(listofdict)
        return veh_list




    def get_vehicle_id(self) -> tuple:
        """Extracts vehicle ids information from simulators response

        :return: tuple containing vehicle ids at current state in all network
        :rtype: list
        """
        return tuple(veh.get('No') for veh in self.get_vehicle_data())

    def query_vehicle_link(self, vehid: int, *args) -> tuple:
        """ Extracts current vehicle link information from simulators response

        :param vehid: vehicle id multiple arguments accepted
        :type vehid: str
        :return: vehicle link in tuple form
        :rtype: tuple
        """
        vehids = set((vehid, *args)) if args else vehid
        vehid_pos = self.query_vehicle_data_dict('Lane\\Link\\No', vehids)
        return tuple(vehid_pos.get(veh) for veh in vehids)

    def query_vehicle_position(self, vehid: int, *args) -> tuple:
        """ Extracts current vehicle distance information from simulators response

        :param vehid: vehicle id multiple arguments accepted
        :type vehid: str
        :return: vehicle distance in link in tuple form
        :rtype: tuple
        """
        vehids = set((vehid, *args)) if args else vehid
        vehid_pos = self.query_vehicle_data_dict('Pos', vehids)
        return tuple(vehid_pos.get(veh) for veh in vehids)

    def query_vehicle_data_dict(self, dataval: str, vehid: int, *args) -> dict:
        """ Extracts and filters vehicle data from the simulators response

        :param dataval: parameter to be extracted e.g. '@id', '@dst'
        :type dataval: str
        :param vehid: vehicle id, multiple arguments accepted
        :type vehid: str
        :return: dictionary where key is @id and value is dataval
        :rtype: dict
        """
        vehids = set((vehid, *args)) if args else set(vehid)
        data_vehs = [(veh.get('No'), veh.get(dataval)) for veh in self.get_vehicle_data() if veh.get('No') in vehids]
        return dict(data_vehs)

    def is_vehicle_in_network(self, vehid: int, *args) -> bool:
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

    def vehicle_in_link(self, link: int, lane: int = 1) -> tuple:
        """Returns a tuple containing vehicle ids traveling on the same link+lane at current state

        :param link: link name
        :type link: int
        :param lane: lane number, defaults to 1
        :type lane: int, optional
        :return: tuple containing vehicle ids
        :rtype: tuple
        """
        return tuple(veh.get('No') for veh in self.get_vehicle_data() if veh.get('Lane\\Link\\No') == link and veh.get('Lane\\Index') == lane)

    def is_vehicle_in_link(self, veh: int, link: int) -> bool:
        """ Returns true if a vehicle is in a link at current state
        
        :param veh: vehicle id
        :type veh: int
        :param link: link name
        :type link: int
        :return: True if veh is in link
        :rtype: bool
        """
        veh_ids = self.vehicle_in_link(link)
        return set(veh).issubset(set(veh_ids))

    def vehicle_downstream_of(self, vehid: int) -> tuple:
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

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos > vehpos)

    def vehicle_upstream_of(self, vehid: int) -> tuple:
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

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos < vehpos)

    def create_vehicle_list(self):
        """Initialize 
        """
        if not self._vehs:
            self._vehs = VehicleList.from_request(self.get_vehicle_data())
            return

    def update_vehicle_list(self):
        """ Construct and or update vehicle data
        """
        if self._vehs:
            self._vehs.update_list(self.get_vehicle_data())
            return
        self.create_vehicle_list()

    def __contains__(self, elem: Vehicle) -> bool:
        return elem in self._vehs

    @property
    def data_query(self):
        try:
            return self._str_response
        except IndexError: # dont know the type of error yet
            return {}

    @property
    def vehicles(self):
        self.update_vehicle_list()
        return self._vehs

    @property
    def current_time(self) -> str:
        return self.data_query.get("INST").get("@val")

    @property
    def current_nbveh(self) -> int:
        return self.data_query.get("INST").get("@nbVeh")
