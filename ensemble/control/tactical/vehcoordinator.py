"""**Vehicle Gap Coordinator**

This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

# ============================================================================
# STANDARD IMPORTS
# ============================================================================

from typing import Union
import numpy as np
from dataclasses import dataclass
from functools import cached_property

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehicle import Vehicle
from ensemble.component.platoon_vehicle import PlatoonVehicle
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)
from ensemble.tools.constants import DCT_PLT_CONST, DCT_RUNTIME_PARAM
from ensemble.metaclass.coordinator import AbsSingleGapCoord
from ensemble.metaclass.controller import AbsController
from ensemble.control.operational.reference import ReferenceHeadway


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

PLState = Union[StandAlone, Platooning, Joining, Splitting]


MAXTRKS = DCT_PLT_CONST["max_platoon_length"]
MAXNDST = DCT_PLT_CONST["max_connection_distance"]
PLT_TYP = DCT_PLT_CONST["platoon_types"]
MAXDSTR = DCT_PLT_CONST["max_gap_error"]

TIME_STEP_OP = DCT_RUNTIME_PARAM["sampling_time_operational"]

KEYS = ("a", "x", "v", "s", "u", "Dv", "Pu", "Ps")


@dataclass
class VehGapCoordinator(AbsSingleGapCoord):

    status: PLState = StandAlone()
    platoon: bool = False
    comv2x: bool = True
    dx_ref: float = 30
    platoonid: int = 0

    # def __new__(cls, **kwargs):
    #     if kwargs.get("create"):
    #         return super(VehGapCoordinator, cls).__new__(cls)
    #     return None

    def __init__(self, vehicle: PlatoonVehicle):
        self.ego = vehicle
        self._fgc = None
        self._rgc = None
        self.positionid = 0

        create_dct = lambda: {key: 0.0 for key in KEYS}
        self._ctr_lead_data = create_dct()
        self._ctr_ego_data = create_dct()
        self._ctr_lead_data["id"] = max(self.ego.vehid - 1, 0)
        self._ctr_ego_data["id"] = self.ego.vehid

        # Historical data
        self._history_state = np.empty((3,))
        self._history_control = np.empty((1,))

    def init_reference(self):
        """Initializes the reference class for the gap coordinator. In particular the initial conditions should be already computed."""
        if hasattr(self, "_reference"):
            return
        if self.leader is self:
            self._reference = ReferenceHeadway()
        else:
            self._reference = ReferenceHeadway(gap0=self.dx)

    @property
    def reference(self):
        return self._reference

    def __hash__(self):
        return hash((type(self), self.ego.vehid))

    def __eq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self.ego == rhs.ego

    def __lt__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self.ego.vehid < rhs.ego.vehid

    def __gt__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self.ego.vehid > rhs.ego.vehid

    def __leq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self.ego.vehid <= rhs.ego.vehid

    def __geq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self.ego.vehid >= rhs.ego.vehid

    def solve_state(self) -> PLState:
        """Logic solver for the platoon state machine."""
        new_state = self.status.next_state(self)
        self.ego.state = new_state
        self.reference.create_time_gap_hwy(new_state)
        return new_state

    @property
    def x(self):
        """Ego current position in link"""
        return self.ego.ttd

    @property
    def leader(self) -> AbsSingleGapCoord:
        """Returns the leader vehicle in the platoon"""
        return self._fgc if self._fgc is not None else self

    @leader.setter
    def leader(self, value: AbsSingleGapCoord):
        """Set the leader vehicle gap coordinator"""
        self._fgc = value

    @property
    def follower(self):
        """Returns the follower vehicle in the platoon"""
        return self._rgc if self._rgc is not None else self.ego

    @property
    def is_head(self):
        """Determines if the vehicle is head of the platoon"""
        return self.leader is self.ego

    @property
    def is_tail(self):
        """Determines if the vehicle is tail of the platoon"""
        return self.follower is self.ego

    @property
    def acceleration(self):
        """Acceleration"""
        return self.ego.acceleration

    @property
    def speed(self):
        """Speed"""
        return self.ego.speed

    @property
    def ttd(self):
        """Total travel time"""
        return self.ego.ttd

    @property
    def vehid(self):
        """Vehicle positions"""
        return self.ego.vehid

    @property
    def dx(self):
        """Ego current headway space"""
        return (
            self.leader.x - self.ego.x
            if self.leader.vehid != self.ego.vehid
            else MAXNDST
        )

    @property
    def dv(self):
        """Ego current differential speed"""
        return self.leader.speed - self.ego.speed

    @property
    def control(self):
        """Ego current control"""
        return self._ctr_ego_data.get("u")

    @property
    def positionid(self):
        """Platoon id 0-index notation to denote position on the platoon"""
        return self._platoonid

    @positionid.setter
    def positionid(self, value):
        """Platoon id 0-index notation to denote position on the platoon"""
        self._platoonid = np.clip(value, 0, MAXTRKS)

    @property
    def history_control(self):
        return self._history_control

    @property
    def last_control(self):
        if len(self._history_control.shape) == 1:
            return self.history_control
        return self._history_control[-1]

    @history_control.setter
    def history_control(self, value: np.ndarray):
        self._history_control = np.vstack((self._history_control, value))

    @property
    def history_state(self):
        return self._history_state

    @property
    def last_state(self):
        if len(self._history_state.shape) == 1:
            return self.history_state
        return self._history_state[-1]

    @history_state.setter
    def history_state(self, value: np.ndarray):
        self._history_state = np.vstack((self._history_state, value))

    @property
    def joinable(self):
        """Checks if a vehicle is joinable"""
        return (
            (self.leader.positionid < MAXTRKS - 1)
            and (self.dx < MAXNDST)
            and self.leader.comv2x
        ) and (self.leader is not self)
        # self.intruder

    @property
    def intruder(self):
        """Returns true when the vehtype of my immediate leader is not platoon"""
        return NotImplementedError

    def cancel_join_request(self, value: bool = False):
        """Forces ego to abandon platoon mode"""
        return not self.joinable or value

    def confirm_platoon(self):
        """Confirms ego platoon mode"""
        return abs(self.dx - self.dx_ref) < MAXDSTR

    @property
    def leader_data(self):
        """Operational leader control data"""
        # Lead updates
        data = {
            "a": self.leader.acceleration,
            "x": self.leader.x,
            "v": self.leader.speed,
            "s": self.leader.dx,
            "u": self.leader.control,
            "Dv": self.leader.dv,
            "Pu": self._ctr_lead_data.get("u"),
            "Ps": self._ctr_lead_data.get("s"),
        }
        self._ctr_lead_data.update(data)
        return self._ctr_lead_data

    @leader_data.setter
    def leader_data(self, value: dict):
        """Operational leader control data (setter) - For manual update. It updates the ego data dictionary to specific values given within a dictionary structure.

        * a: real acceleration
        * x: postition
        * v: speed
        * s: spacing
        * u: control

        * D: delta
        * P: past

        Args:
            value (dict): Dictionary with keys a,x,v,Dv,Pu,Ps

        """
        self._ctr_lead_data.update(value)

    @property
    def ego_data(self):
        """Operational leader control data"""

        # Ego updates
        data = {
            "a": self.acceleration,
            "x": self.x,
            "v": self.speed,
            "s": self.dx,
            "u": self.control,
            "Dv": self.dv,
            "Pu": self._ctr_ego_data.get("u"),
            "Ps": self._ctr_ego_data.get("s"),
        }
        self._ctr_ego_data.update(data)
        return self._ctr_ego_data

    @ego_data.setter
    def ego_data(self, value: dict):
        """Operational ego control data (setter) - For manual update. It updates the ego data dictionary to specific values given within a dictionary structure.

        * a: real acceleration
        * x: postition
        * v: speed
        * s: spacing
        * u: control

        * D: delta
        * P: past

        Args:
            value (dict): Dictionary with keys a,x,v,Dv,Pu,Ps

        """
        self._ctr_ego_data.update(value)

    def get_step_data(self):
        """Retrieves current time data for the operational layer"""

        return self.leader_data, self.ego_data

    def evolve_control(
        self,
        control: AbsController,
        time: float,
        time_step: float = TIME_STEP_OP,
    ):
        """Considers a one chunk of step evolution of the operational control layer

        Args:
            control (AbsController): Operational controller
        """
        control(self, self.reference, time, time_step)
