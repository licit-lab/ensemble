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
import pandas as pd

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .vehicle import Vehicle
from ensemble.logic.frozen_Set import SortedFrozenSet

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class VehicleList(SortedFrozenSet):
    """ Class defining a set of vehicles. This class is based on a sorted 
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

        The list could be eventually updated as an observer but for simplicity reasons it is kept like this. 
    """

    def __init__(self, request):
        self._request = request
        data = [Vehicle(request, **v) for v in request.get_vehicle_data()]
        super().__init__(data)

    def update_list(self):
        """ Update vehicle data according to an update in the request.
        """
        data = self + VehicleList(self._request)
        self._items = data._items

    def _get_vehicles_attribute(self, attribute: str) -> pd.Series:
        """ Retrieve list of parameters 
        
            Args: 
                attribute (str): One of the vehicles attribute e.g. 'distance'
            
            Returns 
                dataframe (series): Returns values for a set of vehicles 
        """
        return self._to_pandas()[attribute]

    @property
    def acceleration(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("acceleration")

    @property
    def speed(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("speed")

    @property
    def distance(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("distance")

    def _to_pandas(self) -> pd.DataFrame:
        """ Transforms vehicle list into a pandas for rendering purposes 
        
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
