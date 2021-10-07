"""
Data Query 
==========
This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc
from typing import Union, Dict, List, Tuple
from collections import defaultdict
from ctypes import create_string_buffer

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.logic.publisher import Publisher
import ensemble.tools.constants as ct

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

vtypes = Union[float, int, str]
vdata = Tuple[vtypes]
vmaps = Dict[str, vtypes]
vlists = List[vmaps]
response = defaultdict(lambda: False)


class DataQuery(Publisher, metaclass=abc.ABCMeta):
    """This general dataquery model implements a general publisher pattern to
    broadcast information towards different subscribers. Subscribers are intented to be objects such as vehicles, front/rear gap coordinators.

    In particular this creates a subject that can notify to a specific channel where subscribers are registered.

    Example:
        Create a DataQuery for 2 type of channels, ``automated`` and  ``regular`` and perform a subscription ::

            >>> channels = ('auto','regular')
            >>> p = Publisher(channels)
            >>> s = Subscriber(p,'auto')  # Registers a s into p
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._str_response = create_string_buffer(ct.BUFFER_STRING)

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return (
            "Sim Time: {}, VehInNetwork: {}".format(
                self.current_time, self.current_nbveh
            )
            if self.get_vehicle_data()
            else "No vehicles detected"
        )

    # =========================================================================
    # MEMORY HANDLING
    # =========================================================================
    @abc.abstractproperty
    def query(self):
        """A method to store data as received from the simulator"""
        pass

    @abc.abstractproperty
    def current_time(self) -> float:
        """Provides current time step"""
        pass

    @abc.abstractproperty
    def current_nbveh(self) -> int:
        """Provides current number of vehicles"""
        pass

    @abc.abstractmethod
    def get_vehicle_data(self) -> vlists:
        """Provides current vehicle data"""
        pass

    @abc.abstractmethod
    def is_vehicle_driven(self) -> bool:
        """True if the vehicle state is exposed to a driven state"""
        pass

    @abc.abstractmethod
    def update_vehicle_registry(self, configurator):
        """Updates the vehicle registry within the stream"""
        pass

    # =========================================================================
    # METHODS
    # =========================================================================

    def dispatch_observers(self):
        """Publishes/dispatch information two all registered elements"""
        for c in self._channels:
            self.dispatch(c)

    def get_vehicles_property(self, property: str) -> vdata:
        """Extracts a specific property and returns a tuple containing this
        property for all vehicles in the buffer string

        Args:
            property (str):
                one of the following options abscissa, acceleration, distance, elevation, lane, link, ordinate, speed, vehid, vehtype,

        Returns:
            values (tuple):
                tuple with corresponding values e.g (0,1), (0,),(None,)
        """
        return tuple(veh.get(property) for veh in self.get_vehicle_data())

    def filter_vehicle_property(self, property: str, *args):
        """Filter out a property for a subset of vehicles

        Args:
            property (str):
                one of the following options abscissa, acceleration, distance, elevation, lane, link, ordinate, speed, vehid, vehtype,

            vehids (int):
                separate the ``vehid`` via commas to get the corresponding property
        """
        if args:
            sargs = set(args)
            vehids = set(self.get_vehicles_property("vehid"))
            fin_ids = vehids.intersection(sargs)
            return tuple(
                veh.get(property)
                for veh in self.get_vehicle_data()
                if veh.get("vehid") in fin_ids
            )
        return self.get_vehicles_property(property)

    def get_vehicle_properties(self, vehid: int) -> dict:
        """Return all properties for a given vehicle id

        Returns:
            vehdata (dict): Dictionary with all vehicle properties
        """
        data = self.get_vehicle_data()
        for v in data:
            if v["vehid"] == vehid:
                return v
        return {}

    def is_vehicle_in_network(self, vehid: int, *args) -> bool:
        """True if veh id is in the network at current state, for multiple
        arguments. True if all veh ids are in the network.

        Args:
            vehid (int): Integer of vehicle id, comma separated if testing for multiple

        Returns:
            present (bool): True if vehicle is in the network otherwise false.

        """
        all_vehs = self.get_vehicles_property("vehid")
        if not args:
            return vehid in all_vehs
        vehids = set((vehid, *args))
        return set(vehids).issubset(set(all_vehs))

    def vehicles_in_link(self, link: str, lane: int = 1) -> vdata:
        """Returns a tuple containing vehicle ids traveling on the same
        (link,lane) at current state

        Args:
            link (str): link name
            lane (int): lane number

        Returns:
            vehs (tuple): set of vehicles in link/lane

        """
        return tuple(
            veh.get("vehid")
            for veh in self.get_vehicle_data()
            if veh.get("link") == link and veh.get("lane") == lane
        )

    def is_vehicle_in_link(self, veh: int, link: str) -> bool:
        """Returns true if a vehicle is in a link at current state

        Args:
            vehid (int): vehicle id
            link (str): link name

        Returns:
            present (bool): True if veh is in link

        """
        veh_ids = self.vehicles_in_link(link)
        return set((veh,)).issubset(set(veh_ids))

    def vehicle_downstream_of(self, vehid: int) -> tuple:
        """Get ids of vehicles downstream to vehid

        Args:
            vehid (str):
                vehicle id

        Returns:
            vehid (tuple):
                vehicles downstream of vehicle id
        """
        link = self.filter_vehicle_property("link", vehid)[0]
        vehpos = self.filter_vehicle_property("distance", vehid)[0]

        vehids = set(self.vehicles_in_link(link))
        neigh = vehids.difference(set((vehid,)))

        neighpos = self.filter_vehicle_property("distance", *neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos > vehpos)

    def vehicle_upstream_of(self, vehid: str) -> tuple:
        """Get ids of vehicles upstream to vehid

        Args:
            vehid (str):
                vehicle id

        Returns:
            vehid (tuple):
                vehicles upstream of vehicle id
        """
        link = self.filter_vehicle_property("link", vehid)[0]
        vehpos = self.filter_vehicle_property("distance", vehid)[0]

        vehids = set(self.vehicles_in_link(link))
        neigh = vehids.difference(set((vehid,)))

        neighpos = self.filter_vehicle_property("distance", *neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos < vehpos)
