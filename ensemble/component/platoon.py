""" 
Platoon List
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

from .truck import Truck
from ensemble.logic.platoon_set import PlatoonSet
from ensemble.tools.constants import DCT_PLT_CONST

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

PLATOON_TYPES = DCT_PLT_CONST.get("platoon_types")


class Platoon(PlatoonSet):
    """ Class defining a set of platoonning vehicles. This class is based on 
        a  frozen set and supports multiple operations in between sets. This operations consider logic to fuse or split two vehicle platoons. This  You can define a list based on a simluator request and the list will update automatically via a single method. 

        Args: 
            request (Publisher): Publisher of information 

        Example: 
            Define a list of vehicles to trace the requests ::
                >>> simrequest = SimulatorRequest()
                >>> simrequest.query = one_vehicle_xml
                >>> vl = PlatoonSet(simrequest)
                >>> simrequest.query = second_vehicle_xml
                >>> vl.update_list() # This updates manually

        The list could be eventually updated as an observer but for simplicity reasons it is kept like this. 
    """

    def __init__(self, request):
        self._request = request
        data = [
            Truck(request, **v)
            for v in request.get_vehicle_data()
            if v["vehid"] in PLATOON_TYPES
        ]
        super().__init__(data)

    def update_list(self):
        """ Update vehicle data according to an update in the request.
        """
        data = self + PlatoonSet(self._request)
        self._items = data._items

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
