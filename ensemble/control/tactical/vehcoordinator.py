"""**Vehicle Gap Coordinator**

This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from typing import Union
import numpy as np
from dataclasses import dataclass

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehicle import Vehicle
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)
from ensemble.tools.constants import DCT_PLT_CONST
from ensemble.metaclass.coordinator import AbsSingleGapCoord

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

PLState = Union[StandAlone, Platooning, Joining, Splitting]


MAXTRKS = DCT_PLT_CONST["max_platoon_length"]
MAXNDST = DCT_PLT_CONST["max_connection_distance"]
PLT_TYP = DCT_PLT_CONST["platoon_types"]
MAXDSTR = DCT_PLT_CONST["max_gap_error"]


@dataclass
class VehGapCoordinator(AbsSingleGapCoord):

    status: PLState = StandAlone()
    platoon: bool = False
    comv2x: bool = True
    dx_ref: float = 30
    platoonid: int = 0

    def __init__(self, vehicle: Vehicle):
        self.ego = vehicle
        self._fgc = None
        self._rgc = None
        self.positionid = 0
        # self.solve_fgc_state()

    def __hash__(self):
        return hash((type(self), self.ego.vehid))

    def solve_state(self) -> PLState:
        """Logic solver for the platoon state machine."""
        return self.status.next_state(self)

    @property
    def x(self):
        """ Ego current position in link """
        return self.ego.distance

    @property
    def leader(self):
        """ Returns the leader vehicle in the platoon"""
        return self._fgc if self._fgc is not None else self

    @leader.setter
    def leader(self, value: AbsSingleGapCoord):
        """ Set the leader vehicle gap coordinator"""
        self._fgc = value

    @property
    def follower(self):
        """ Returns the follower vehicle in the platoon"""
        return self._rgc if self._rgc is not None else self.ego

    @property
    def is_head(self):
        """ Determines if the vehicle is head of the platoon"""
        return self.leader is self.ego

    @property
    def is_tail(self):
        """ Determines if the vehicle is tail of the platoon """
        return self.follower is self.ego

    @property
    def ttd(self):
        """ Total travel time"""
        return self.ego.ttd

    @property
    def vehid(self):
        """ Vehicle positions"""
        return self.ego.vehid

    @property
    def dx(self):
        """ Ego current headway space"""
        return (
            self.leader.ttd - self.ego.ttd
            if self.leader.vehid != self.ego.vehid
            else MAXNDST
        )

    @property
    def positionid(self):
        """ Platoon id 0-index notation to denote position on the platoon"""
        return self._platoonid

    @positionid.setter
    def positionid(self, value):
        """ Platoon id 0-index notation to denote position on the platoon"""
        self._platoonid = np.clip(value, 0, MAXTRKS)

    @property
    def joinable(self):
        """ Checks if a vehicle is joinable"""
        return (
            (self.leader.positionid < MAXTRKS - 1)
            and (self.dx < MAXNDST)
            and self.leader.comv2x
        ) and (self.leader is not self)
        # self.intruder

    @property
    def intruder(self):
        """ Returns true when the vehtype of my immediate leader is not platoon"""
        return NotImplementedError

    def cancel_join_request(self, value: bool = False):
        """ Forces ego to abandon platoon mode"""
        return not self.joinable or value

    def confirm_platoon(self):
        """ Confirms ego platoon mode"""
        return abs(self.dx - self.dx_ref) < MAXDSTR
