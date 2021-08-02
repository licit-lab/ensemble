""" 
Vehicle Model
=============
This module implements a vehicle model.

Vehicle model acts as an instance to trace individual vehicle data and modify vehicle behavior according to given dynamics
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import Dict, List
import itertools
import numpy as np
from dataclasses import dataclass, field

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.logic.subscriber import Subscriber
from ensemble.tools import constants as ct
from ensemble.metaclass.stream import DataQuery
from ensemble.metaclass.dynamics import AbsDynamics

from ensemble.handler.symuvia.stream import SimulatorRequest
from ensemble.component.dynamics import SampleDynamics

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

sample_dynamics = SampleDynamics()


@dataclass
class Vehicle(Subscriber):
    """Vehicle class defined for storing data on a single vehicle:

    You need a Publisher from where the vehicle is going to take data:

    Args:
        request (Publisher): Parser or object publishing data

    Retunrns:
        vehicle (Vehicle): A Dataclass with vehicle parameters

    ============================  =================================
    **Variable**                  **Description**
    ----------------------------  ---------------------------------
    ``abscissa``                    Current coordinate on y axis
    ``acceleration``                Current acceleration
    ``distance``                    Current distance traveled on link
    ``elevation``                   Current elevation
    ``lane``                        Current lane
    ``link``                        Current road vehicle is traveling
    ``ordinate``                    Current coordinate x axis
    ``speed``                       Current speed
    ``vehid``                       Vehicle id
    ``vehtype``                     Vehicle class
    ============================  =================================

    Example:
        This is one example on how to register a new vehicle ::

        >>> req = SimulatorRequest()
        >>> veh = Vehicle(req)
        >>> req.dispatch() # This will update vehicle data

    When having multiple vehicles please indicate the `vehid` before launching the dispatch method. This is because the vehicle object is looks for a vehicle id within the data.

    Example:
        This is one example on how to register two vehicles ::

        >>> req = SimulatorRequest()
        >>> veh1 = Vehicle(req, vehid=0)
        >>> veh2 = Vehicle(req, vehid=1)
        >>> req.dispatch() # This will update vehicle data on both vehicles


    """

    counter = itertools.count()
    abscissa: float = 0.0
    acceleration: float = 0.0
    distance: float = 0.0
    driven: bool = False
    elevation: float = 0.0
    lane: int = 1
    link: str = "Zone_001"
    ordinate: float = 0.0
    speed: float = 25.0
    vehid: int = 0
    vehtype: str = ""

    def __init__(
        self,
        request: DataQuery,
        dynamics: AbsDynamics = sample_dynamics,
        **kwargs
    ):
        """This initializer creates a Vehicle"""
        # Undefined properties
        self.count = next(self.__class__.counter)
        self.dynamics = dynamics
        self.itinerary = []

        # Internal
        self._ttdprev = 0
        self._ttdpivot = 0

        # Optional properties
        self.update_no_request(**kwargs)

        super().__init__(request)

    def __hash__(self):
        return hash((type(self), self.vehid))

    def __eq__(self, veh):
        if not isinstance(veh, type(self)):
            return NotImplemented
        return self.vehid == veh.vehid

    def update(self):
        """Updates data from publisher"""
        dataveh = self._publisher.get_vehicle_properties(self.vehid)
        self.__dict__.update(**dataveh)

        link = getattr(self, "link")
        if link not in getattr(self, "itinerary"):
            self.itinerary.append(link)

    def update_no_request(self, **kwargs):
        """Update vehicle data from specific keyword arguments"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def state(self) -> np.ndarray:
        """Returns current state of the vehicle

        Returns:
            np.ndarray: [3d-array] @ k+1 [distance;speed;acceleration]
        """
        return np.array((self.distance, self.speed, self.acceleration))

    @property
    def x(self):
        """Return vehicle travelled ditance"""
        return self.distance

    @property
    def v(self):
        """Return vehicle speed"""
        return self.speed

    @property
    def a(self):
        """Return vehicle acceleration"""
        return self.acceleration

    @property
    def ttd(self):
        """Total travel distance by a single vehicle"""
        # this is for the full sequence functionality we need something for a step by step thing. So the idea is that it should check the internals of the for condition, we should keep the pivot, prev, dist as values
        # pivot = 0
        # prev = 0
        # dist = 0
        # lst = []
        # for i in seq:
        #     if i <= prev:
        #         print(f"Prev {prev}, Current {i}")
        #         pivot += prev
        #         print(f"Now pivot {pivot}")
        #     dist = pivot + i
        #     print(f"Current {dist}")
        #     prev = i
        #     lst.append(dist)
        # return lst

        if self.x < self._ttdprev:
            self._ttdpivot += self._ttdprev
        self._ttddist = self._ttdpivot + self.x
        self._ttdprev = self.x
        return self._ttddist


if __name__ == "__main__":
    # Run from base folder
    import os

    truck_path = os.path.join(
        os.getcwd(), "ensemble", "libs", "darwin", "truckDynamics.dylib"
    )

    sim = SimulatorRequest()
    veh = Vehicle(sim)
