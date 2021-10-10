""" 
Vehicle List
=============
This module implements a vehicle list model.

Vehicle list is a collection implementation that acts as an instance to trace individual vehicle data of several vehicles.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from dataclasses import asdict
from typing import Iterable, Union
import pandas as pd
import numpy as np
from itertools import groupby

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehicle import Vehicle
from ensemble.component.platoon_vehicle import PlatoonVehicle
from ensemble.tools.constants import DCT_PLT_CONST

from ensemble.logic.frozen_set import SortedFrozenSet
from ensemble.logic.publisher import Publisher
from ensemble.tools.geometry import Point

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

PLT_TYPE = DCT_PLT_CONST["platoon_types"]
EMPTY_MESSAGE = "\tNo vehicles have been registered"
VehType = Union[Vehicle, PlatoonVehicle]


class VehicleList(SortedFrozenSet, Publisher):
    """Class defining a set of vehicles. This class is based on a sorted
    frozen set and supports multiple operations in between sets. You can define a list based on a simluator request and the list will update automatically via a single method.

    Args:
        request (Publisher): Publisher of information

    Example:
        Define a list of vehicles to trace the requests ::
            >>> simrequest = SimulatorRequest()
            >>> simrequest.query = one_vehicle_xml
            >>> vl = VehicleList(simrequest)
            >>> simrequest.query = second_vehicle_xml
            >>> vl.update_list() # This updates manually

    Example:
        Define a list of vehicles to be used manually::
            >>> simrequest = SimulatorRequest()
            >>> vl = VehicleList(simrequest)
            >>> v1 = Vehicle(simrequest, vehid=1)
            >>> v2 = Vehicle(simrequest, vehid=2)
            >>> vl.update_list(optional=[v1,v2]) # Adds vehicles to the list
    The list could be eventually updated as an observer but for simplicity reasons it is kept like this.
    """

    _cumul = set()

    def __init__(self, request):
        self._request = request
        data = (
            PlatoonVehicle(request, **v)
            if v.get("vehtype") in PLT_TYPE
            else Vehicle(request, **v)
            for v in request.get_vehicle_data()
        )
        self._free = []
        self.__class__._cumul = self.__class__._cumul.union(
            request.get_vehicles_property("vehid")
        )
        SortedFrozenSet.__init__(self, tuple(data))
        Publisher.__init__(self)

    def update_list(self, extra=[]):
        """Update vehicle data according to an update in the request."""
        newveh = []
        # Create only new vehicles
        for v in self._request.get_vehicle_data():
            if v.get("vehid") not in self.__class__._cumul:
                if v.get("vehtype") in PLT_TYPE:
                    newveh.append(PlatoonVehicle(self._request, **v))
                    self.__class__._cumul.add(v.get("vehid"))
                else:
                    newveh.append(Vehicle(self._request, **v))
                    self.__class__._cumul.add(v.get("vehid"))
                lead = self.get_leader(newveh[-1])
                newveh[-1].leadid = lead.vehid
                follow = self.get_follower(newveh[-1])
                newveh[-1].followid = follow.vehid
        data = SortedFrozenSet(self._items).union(newveh)
        data = data.union(extra)

        # Put vehicles on list
        self._items = data._items

        # Take out exciting vehicles
        for veh in self._items:
            if veh.vehid not in self._request.get_vehicles_property("vehid"):
                self.release(veh)

        # Publish for followers
        self.dispatch()
        self.update_leaders()
        self.update_followers()

    def check_and_release(self, veh: VehType):
        """Checks wether a vehicle is inside the file and then releases the vehicle

        Args:
            veh (VehType): Vehicle object
        """

    def release(self, veh: VehType):
        """Moves a vehicle to a free list so that it is not considered in the

        Args:
            r (VehType): Vehicle object
        """
        self._items.remove(veh)
        self.__class__._cumul.remove(veh.vehid)
        self._free.append(veh)

    def _get_vehicles_attribute(self, attribute: str) -> pd.Series:
        """Retrieve list of parameters

        Args:
            attribute (str): One of the vehicles attribute e.g. 'distance'

        Returns
            dataframe (series): Returns values for a set of vehicles
        """
        return self.pandas_print()[attribute]

    @property
    def acceleration(self) -> pd.Series:
        """Returns all vehicle's accelerations"""
        return self._get_vehicles_attribute("acceleration")

    @property
    def speed(self) -> pd.Series:
        """Returns all vehicle's accelerations"""
        return self._get_vehicles_attribute("speed")

    @property
    def distance(self) -> pd.Series:
        """Returns all vehicle's accelerations"""
        return self._get_vehicles_attribute("distance")

    @property
    def link(self) -> pd.Series:
        """Returns all vehicle's link"""
        return self._get_vehicles_attribute("link")

    @property
    def lane(self) -> pd.Series:
        """Returns all vehicle's lane"""
        return self._get_vehicles_attribute("lane")

    @property
    def abscissa(self) -> pd.Series:
        """Returns all vehicle's abscissa"""
        return self._get_vehicles_attribute("abscissa")

    @property
    def ordinate(self) -> pd.Series:
        """Returns all vehicle's ordinate"""
        return self._get_vehicles_attribute("ordinate")

    @property
    def vehid(self) -> pd.Series:
        """Returns all vehicle's vehid"""
        return self._get_vehicles_attribute("vehid")

    @property
    def leadid(self) -> pd.Series:
        """Returns all leader vehicle's vehid"""
        return self._get_vehicles_attribute("leadid")

    def distance_filter(
        self,
        ego: Vehicle,
        type: str = "downstream",
        property="distance",
        radius: float = 100,
    ):
        """
        Returns all vehicles' downstream or
        """
        case = {
            "downstream": {
                getattr(v, "vehid"): getattr(v, property)
                for v in self._items
                if v.distance > ego.distance
                and v.distance < ego.distance + radius
            },
            "upstream": {
                getattr(v, "vehid"): getattr(v, property)
                for v in self._items
                if v.distance < ego.distance
                and v.distance > ego.distance - radius
            },
            "all": {
                getattr(v, "vehid"): getattr(v, property)
                for v in self._items
                if np.linalg.norm(
                    [v.abscissa - ego.abscissa, v.ordinate - ego.ordinate]
                )
                < radius
            },
        }
        return case.get(type)

    def get_leader(self, ego: Vehicle, distance: float = 100) -> Vehicle:
        """Returns ego vehicle immediate leader"""

        downstreamdistance = self.distance_filter(
            ego, "downstream", property="_distance", radius=distance
        )

        # Former case, if we detect vehicles downstream
        if downstreamdistance:
            array = np.array(tuple(downstreamdistance.values()))
            idx = (np.abs(array - ego.distance)).argmin()
            closest = array[idx]
            veh = [v for v in self._items if v.distance == closest]
            ego.leadid = veh[0].vehid
            return veh[0]

        radiusids = self.distance_filter(
            ego, "all", property="lane", radius=distance
        )

        # Get the average points beyond
        ego_pos = Point(ego.abscissa, ego.ordinate)
        points_in_radious = {
            x.vehid: Point(x.abscissa, x.ordinate).isinfrontof(ego_pos)
            for x in self
            if x.vehid != ego.vehid and x.vehid in radiusids.keys()
        }

        if points_in_radious == {}:
            # No vehicles in radious or I am traveling alone
            ego.leadid = ego.vehid
            return ego

        candidates = {
            x.vehid: ego_pos.distanceto(Point(x.abscissa, x.ordinate))
            for x in self._items
            if ego_pos.isbehindof(Point(x.abscissa, x.ordinate))
        }

        if candidates == {}:
            # No points beyond so I am my leader with followers
            ego.leadid = ego.vehid
            return ego

        distances = np.asarray(list(candidates.values()))
        idx = distances.argmin()
        leader = self[list(candidates.keys())[idx]]

        ego.leadid = leader.vehid
        return leader

    def update_leaders(self):
        """Updates all vehicles leaders"""
        for veh in self:
            self.get_leader(veh)

    def get_follower(self, ego: Vehicle, distance: float = 100) -> Vehicle:
        """
        Returns ego vehicle immediate follower
        """
        upstreamdistance = self.distance_filter(
            ego, "upstream", property="distance", radius=distance
        )

        # Former case, if we detect vehicles upstream
        if upstreamdistance:
            array = np.array(tuple(upstreamdistance.values()))
            idx = (np.abs(array - ego.distance)).argmin()
            closest = array[idx]
            veh = [v for v in self._items if v.distance == closest]
            ego.followid = veh[0].vehid
            return veh[0]

        radiusids = self.distance_filter(
            ego, "all", property="lane", radius=distance
        )

        # Get the average points behind
        ego_pos = Point(ego.abscissa, ego.ordinate)
        points_in_radious = {
            x.vehid: Point(x.abscissa, x.ordinate).isbehindof(ego_pos)
            for x in self
            if x.vehid != ego.vehid and x.vehid in radiusids.keys()
        }

        if points_in_radious == {}:
            # No vehicles in radious or I am traveling alone
            ego.followid = ego.vehid
            return ego

        candidates = {
            x.vehid: ego_pos.distanceto(Point(x.abscissa, x.ordinate))
            for x in self._items
            if ego_pos.isinfrontof(Point(x.abscissa, x.ordinate))
        }

        if candidates == {}:
            # No points beyond so I am my leader with followers
            ego.followid = ego.vehid
            return ego

        distances = np.asarray(list(candidates.values()))
        idx = distances.argmin()
        follower = self[list(candidates.keys())[idx]]

        ego.followid = follower.vehid
        return follower

    def update_followers(self):
        """Updates all vehicles followers"""
        for veh in self:
            self.get_follower(veh)

    def pandas_print(self, columns: Iterable = []) -> pd.DataFrame:
        """Transforms vehicle list into a pandas for rendering purposes

        Returns:
            df (DataFrame): Returns a table with pandas data.

        """
        df = pd.DataFrame([asdict(v) for v in self._items])
        return df[columns] if (columns and not df.empty) else df

    def pretty_print(self, columns: list = []) -> str:
        """Summary of info"""
        df = self.pandas_print(["vehid"] + columns)
        return EMPTY_MESSAGE if df.empty else str(df)

    def __str__(self):
        if not self._items:
            return EMPTY_MESSAGE
        df = self.pandas_print()
        return EMPTY_MESSAGE if df.empty else str(df)

    def __repr__(self):
        if not self._items:
            return EMPTY_MESSAGE
        df = self.pandas_print()
        return EMPTY_MESSAGE if df.empty else str(df)

    def __iter__(self):
        """Protocol sorting data by largest distance on link"""
        self.__tmpit = iter(
            sorted(self._items, key=lambda x: x.distance, reverse=True)
        )
        return self.__tmpit

    def __next__(self):
        return next(self.__tmpit)

    def iterate_links_distances(self):
        """Special iterator for vehicle list by considering link ordering"""

        f = lambda x: x.link

        lttd = sorted(self._items, key=lambda x: x.ttd, reverse=True)

        for link, group_veh in groupby(lttd, f):
            for gc in group_veh:
                yield gc, link
