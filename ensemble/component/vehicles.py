""" 
    Implements a set of classes to manage vehicles within the API. The classes include a representation of single vehicle model with dynamic evolution, the set of ordered vehicles within a specific time step in the simulation, and indicators about the total amount of vehicles cumulated on the simulator. 

    Vehicle model acts as an object to store vehicle data and provide specific behaviors required by the driver model in the form of a model :math:`x_i(k+1) = f (x_i(k), u(k), x_{i-1}(k))`

    VehicleList is an ordered frozen set (ordered by id) for which it is possible to iterate at specific time instant to determine specific indicators or particular information of the set of vehicles. 

    VehicleIndicator is an objec in charge of computing indicator for a single vehicle.

    VehicleListIndicators is an object designed for computing indicators over a set of vehicles.  
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import Dict, List
from collections import OrderedDict
import itertools
import numpy as np
import pandas as pd

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import ensemble.tools.constants as ct
from .dynamics import VehicleDynamic
from ensemble.control.tactical.gapcordinator import FrontGap, RearGap

from ensemble.tools.sorted_frozen_set import SortedFrozenSet

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Vehicle:
    """
        Vehicle object defining properties and methods required to store and compute predictions according to a vehicle model. 

        Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

        Args:

            abscissa (float):   x coordinate [m],
            acceleration (float):   Acceleration [m/s2],
            distance (float):   Distance [m],
            vehid (int):   Unique vehicle identifier,
            ordinate (float):  y coorindate [m],
            link (str):  Link name,
            vehtype (str):  Vehicle type,
            speed (float):  speed [m/s],
            lane (int):  lane (from right to left),
            elevation (float):  elevation [m],
            dynamic (VehicleDynamic): Vehicle dynamics (check )
            itinerary (list):  list of ordered links in the network [list],           

    """

    counter = itertools.count()

    def __init__(
        self, abscissa=ct.DCT_VEH_DATA["abscissa"], acceleration=ct.DCT_VEH_DATA["acceleration"], distance=ct.DCT_VEH_DATA["distance"], vehid=ct.DCT_VEH_DATA["vehid"], ordinate=ct.DCT_VEH_DATA["ordinate"], link=ct.DCT_VEH_DATA["link"], vehtype=ct.DCT_VEH_DATA["vehtype"], speed=ct.DCT_VEH_DATA["speed"], lane=ct.DCT_VEH_DATA["lane"], elevation=ct.DCT_VEH_DATA["elevation"], dynamic=VehicleDynamic(), itinerary=ct.DCT_VEH_DATA["itinerary"],
    ):
        """ This initializer creates a Vehicle
        """
        self.abscissa = abscissa
        self.acceleration = acceleration
        self.distance = distance
        self.vehid = vehid
        self.ordinate = ordinate
        self.link = link
        self.vehtype = vehtype
        self.speed = speed
        self.lane = lane
        self.elevation = elevation
        self.dynamic = dynamic
        self.itinerary = itinerary

    def __repr__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def update_state(self, dataveh):
        """Updates data within the structure with 
        
        :param dataveh: vehicle 
        :type dataveh: Vehicle
        """
        self.__dict__.update(**dataveh)

        link = getattr(self, "link")
        if link not in getattr(self, "itinerary"):
            self.itinerary.append(link)

    @property
    def C(self):
        """Output matrix"""
        return self.__output_matrix

    def activate_sensor(self, **kwargs) -> None:
        """Define the observation matrix and observed states in the vehicle vehicle.activate_sensor(speed=True,position=True)
        
        :return: Set the observation matrix __output_matrix
        :rtype: None
        """
        dct_idx = {"position": 0, "speed": 1, "acceleration": 2}
        C = np.zeros([len(kwargs.keys()), 3])
        for key in kwargs.keys():
            idx = dct_idx.get(key)
            C[idx][idx] = kwargs.get(key, 0)
        self.__output_matrix = C

    @property
    def vector_state(self) -> np.array:
        """Vehicle state vector (x,v,a)"""
        return np.array((self.distance, self.speed, self.acceleration))

    @property
    def observed_state(self) -> np.array:
        """ Return observed states via C@(x,v,a)"""
        return self.C @ self.vector_state

    def predict_state(self, control) -> np.array:
        """ Return predicted states via self.dynamic"""
        return self.dynamic(self, control)

    @staticmethod
    def format_dict(dataveh: OrderedDict) -> dict:
        """ This function creates the dictionary 
               {"abscissa":       float(data),
                "acceleration":  float(data),
                "distance":      float(data),
                "vehid":         int(data),
                "ordinate":      float(data),
                "link":          str (data),
                "vehtype":       str (data),
                "speed":         float(data),
                "lane":          int (data),
                "elevation":     float(data),
               } 
        
        :param dataveh: Ordered Dictionary from XML query
        :type dataveh: OrderedDict
        :return: Dictionary as in description
        :rtype: [type]
        """
        data = {
            ct.FIELD_DATA[key]: ct.FIELD_FORMAT[key](val)
            for key, val in dataveh.items()
        }
        return data

    @classmethod
    def from_response(cls, dataveh: OrderedDict):
        """Constructor for the class from a specific dictionary
        
        :param dataveh: Ordered dictionary from XML query
        :type dataveh: OrderedDict
        :return: Vehicle object
        :rtype: [type]
        """
        try:
            return cls(**Vehicle.format_dict(dataveh))
        except KeyError:
            return Vehicle(**dataveh)


lstordct = List[OrderedDict]
lstvehs = List[Vehicle]


class VehicleList:

    """Class for defining a list of vehicles
    """

    def __init__(self, newvehs: lstvehs):
        self.vehicles = {}
        for veh in newvehs:
            self.vehicles[veh.vehid] = veh

    def update_list(self, current_vehs: lstordct):
        """ Appends a new list of vehicles

        :param vehlist: List of vehicles
        :type vehlist: lstordct
        """
        # Reformating data in vehicle dict
        current_vehs = [Vehicle.format_dict(veh) for veh in current_vehs]

        for veh in current_vehs:
            veh_id = veh.get("vehid")
            if veh_id in self.vehicles.keys():
                # Update existing vehicle
                self.vehicles.get(veh_id).update_state(veh)
            else:
                # Create a new vehicle and append
                self.vehicles[veh_id] = Vehicle(**veh)

    def _get_vehicles_attribute(self, attribute: str) -> np.array:
        """ Retrieve list of parameters 
        
        :param attribute: One of the vehicles attribute e.g. 'distance'
        :type attribute: str
        :return: vector of all parameters
        :rtype: np.array
        """
        constructor, ftype = ct.FIELD_FORMATAGG[attribute]
        if ftype:
            return constructor(
                [getattr(veh, attribute) for veh in self], dtype=ftype
            )
        return [getattr(veh, attribute) for veh in self]  # Case str

    @property
    def acceleration(self):
        return self._get_vehicles_attribute("acceleration")

    @property
    def speed(self):
        return self._get_vehicles_attribute("speed")

    @property
    def distance(self):
        return self._get_vehicles_attribute("distance")

    def _to_pandas(self) -> pd.DataFrame:
        """ Transforms vehicle list into a pandas for rendering purposes 
        
        :return: Returns a table with pandas data.
        :rtype: pd.DataFrame
        """

        df_print = pd.DataFrame()
        for key, value in self.vehicles.items():
            df_print = df_print.append(
                pd.DataFrame(value.__dict__, index=(key,))
            )
        return df_print

    def __str__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        df_to_print = self._to_pandas()
        return str(df_to_print)

    def __repr__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        df_to_print = self._to_pandas()
        return repr(df_to_print)

    def __iter__(self):
        self.iterveh = iter(self.vehicles.values())
        return self

    def __next__(self):
        return next(self.iterveh)

    def __contains__(self, veh: Vehicle):
        return veh.vehid in self.get_vehid

    def __getitem__(self, key: int):
        return self.vehicles[key]

    @classmethod
    def from_request(cls, vehlistdct: lstordct):
        """Constructs a vehicle list from a list of ordered dictionaries (simulator repsonse)

        :param vehlist: list containing vehicle data in ordered dict format
        :type vehlist: list
        :return: vehicle list containing list of vehicle data classes
        :rtype: VehicleList
        """
        return cls([Vehicle.from_response(d) for d in vehlistdct])

    @property
    def get_vehid(self):
        return [v.vehid for v in self.vehicles]
