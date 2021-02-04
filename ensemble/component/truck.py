""" 
Platoon List
=============
This module implements a platoon list model.

Platoon list is a collection implementation that acts as an instance to trace individual vehicle data of several platoon vehicles.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from dataclasses import dataclass, field
from ensemble.handler.symuvia.stream import SimulatorRequest


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .vehicle import Vehicle
from ensemble.metaclass.state import AbsState
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


# @dataclass
class Truck(Vehicle):
    """ Vehicle class defined for storing data on a single vehicle: 

        You need a Publisher from where the vehicle is going to take data: 

        Args: 
            request (Publisher): Parser or object publishing data
        
        Retunrns: 
            vehicle (Vehicle): A Dataclass with vehicle parameters

        ============================  =================================
        **Variable**                  **Description**
        ----------------------------  ---------------------------------

        ============================  =================================
        
    """

    def __init__(self, request, **kwargs):
        self.status = StandAlone
        super().__init__(request, **kwargs)

    def __hash__(self):
        return hash((type(self), self.vehid))

    def __eq__(self, veh):
        if not isinstance(veh, type(self)):
            return NotImplemented
        return self.vehid == veh.vehid

    @property
    def leader(self):
        """ Returns leader vehicle object"""
        if self._list:
            return self._list[self.pos - 1]
        return self

    @property
    def dv(self):
        """ Return leader-ego speed difference"""
        return self.leader.v - self.v

    @property
    def dx(self):
        """ Returns leader-ego headway space"""
        return self.leader.x - self.x

    def joinable(self):
        """ Returns a boleean value indicating when the vehicle is joinable"""
        return
