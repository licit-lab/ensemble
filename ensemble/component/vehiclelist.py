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
from typing import Union
import pandas as pd
import numpy as np

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehicle import Vehicle
from ensemble.component.platoon_vehicle import PlatoonVehicle
from ensemble.tools.constants import DCT_PLT_CONST

from ensemble.logic.frozen_set import SortedFrozenSet
from ensemble.logic.publisher import Publisher

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

PLT_TYPE = DCT_PLT_CONST["platoon_types"]

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
        self.__class__._cumul = self.__class__._cumul.union(request.datatraj.id)
        SortedFrozenSet.__init__(self, tuple(data))
        Publisher.__init__(self)

    def update_list(self, extra=[]):
        """Update vehicle data according to an update in the request."""
        newveh = []
        # Create only new vehicles
        for v in self._request.get_vehicle_data():
            if (v.get("vehtype") in PLT_TYPE) and (
                v.get("vehid") not in self.__class__._cumul
            ):
                newveh.append(PlatoonVehicle(self._request, **v))
                self.__class__._cumul.add(v.get("vehid"))
        data = SortedFrozenSet(self._items).union(newveh)
        data = data.union(extra)

        # Put vehicles on list
        self._items = data._items

        # Take out exciting vehicles
        for veh in self._items:
            if veh.vehid not in self._request.datatraj.vehid:
                self.release(veh)

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
        return self._to_pandas()[attribute]

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

    def distance_filter(
        self, ego: Vehicle, type: str = "downstream", radius: float = 100
    ):
        """
        Returns all vehicles' downstream or
        """
        case = {
            "downstream": [
                v.distance
                for v in self._items
                if v.distance > ego.distance
                and v.distance < ego.distance + radius
            ],
            "upstream": [
                v.distance
                for v in self._items
                if v.distance < ego.distance
                and v.distance > ego.distance - radius
            ],
        }
        return case.get(type)

    def get_leader(self, ego: Vehicle, distance: float = 100) -> Vehicle:
        """
        Returns ego vehicle immediate leader
        """
        array = np.asarray(self.distance_filter(ego, "downstream", distance))
        if array.size > 0:
            idx = (np.abs(array - ego.distance)).argmin()
            closest = array[idx]
            veh = [v for v in self._items if v.distance == closest]
            return veh[0]

    def get_follower(self, ego: Vehicle) -> Vehicle:
        """
        Returns ego vehicle immediate leader
        """
        array = np.asarray(self.distance_filter(ego, "upstream"))
        if array.size > 0:
            idx = (np.abs(array - ego.distance)).argmin()
            closest = array[idx]
            veh = [v for v in self._items if v.distance == closest]
            return veh[0]

    def _to_pandas(self) -> pd.DataFrame:
        """Transforms vehicle list into a pandas for rendering purposes

        Returns:
            df (DataFrame): Returns a table with pandas data.

        """
        return pd.DataFrame([asdict(v) for v in self._items])

    def __str__(self):
        if not self._items:
            return "No vehicles have been registered"
        return str(self._to_pandas())

    def __repr__(self):
        if not self._items:
            return "No vehicles have been registered"
        return repr(self._to_pandas())

    def __iter__(self):
        """Protocol sorting data by largest distance on link"""
        self.__tmpit = iter(
            sorted(self._items, key=lambda x: x.distance, reverse=True)
        )
        return self.__tmpit

    def __next__(self):
        return next(self.__tmpit)
