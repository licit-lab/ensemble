"""
    This module contains objects that implement the operational control layer for an individual truck by calling the the compiled shared library ``OperationalDLL``
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from dataclasses import dataclass, field
import pandas as pd
from ctypes import c_double, cdll, c_long, c_int, CDLL, byref
import numpy as np

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.constants import DEFAULT_CACC_PATH, DCT_RUNTIME_PARAM
from ensemble.metaclass.controller import AbsController
from ensemble.control.operational.reference import ReferenceHeadway
from ensemble.control.tactical.vehcoordinator import VehGapCoordinator
from ensemble.metaclass.dynamics import AbsDynamics

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================
TIME_STEP_OP = DCT_RUNTIME_PARAM["sampling_time_operational"]


@dataclass
class CACC(AbsController):
    """This class performs a call to the cacc dynamic shared library.

    Args:
        curr_lead_veh_acceleration (c_double): Leader current acceleration (m/s²).
        curr_lead_veh_id (c_long): Leader vehicle id (-1 no leader).
        curr_lead_veh_rel_velocity (c_long): Leader relative speed w.r.t leader.
        curr_lead_veh_type (c_long): Leader vehicle type.
        curr_timestep (c_double): Current time step (seconds).
        curr_ts_length (c_double): Sampling time (seconds).
        curr_veh_id (c_long): Ego vehicle id.
        curr_veh_setspeed (c_double): Ego cruise control set speed?
        curr_veh_type (c_long): Ego vehicle type.
        curr_veh_controller_in_use (c_long): Control in use 1-ACC ,2-CACC.
        curr_veh_ACC_h (c_double): ACC headway reference.
        curr_veh_CACC_h (c_double): CACC headway reference.
        curr_veh_used_distance_headway (c_double): Ego distance headway (m).
        curr_veh_used_rel_vel (c_double): Ego relative speed w.r.t leader.
        curr_veh_velocity (c_double): Ego speed (m/s).
        curr_veh_autonomous_operational_warning (c_long): From output
        curr_veh_platooning_max_acceleration (c_double): Max acceleration >0 (m/s²).
        prev_veh_cc_setpoint (c_double): Desired speed (m/s).
        prev_veh_cruisecontrol_acceleration (c_double):  From output
        prev_veh_distance_headway (c_double): Past distance headway
        prev_veh_executed_acceleration: Past control output
    """

    # Leader information
    # --------------------------------------------------------------------------
    curr_lead_veh_acceleration: c_double = field(
        default=c_double(0),
        repr=False,
    )
    curr_lead_veh_id: c_long = field(
        default=c_long(-1),
        repr=False,
    )
    curr_lead_veh_rel_velocity: c_double = field(
        default=c_double(0),
        repr=False,
    )
    curr_lead_veh_type: c_long = field(
        default=c_long(1),
        repr=False,
    )

    # Current time info
    # --------------------------------------------------------------------------
    curr_timestep: c_double = field(
        default=c_double(0),
        repr=False,
    )
    curr_ts_length: c_double = field(
        default=c_double(TIME_STEP_OP),
        repr=False,
    )  # seconds

    # Ego info
    # --------------------------------------------------------------------------
    curr_veh_id: c_long = field(
        default=c_long(0),
        repr=False,
    )
    curr_veh_type: c_long = field(
        default=c_long(1),
        repr=False,
    )

    # Speed setpoint
    # --------------------------------------------------------------------------
    curr_veh_setspeed: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Control under use: 1-ACC ,2-CACC
    # --------------------------------------------------------------------------
    curr_veh_controller_in_use: c_long = field(
        default=c_long(2),
        repr=False,
    )

    # Setpoint timegap headways
    # --------------------------------------------------------------------------
    curr_veh_ACC_h: c_double = field(
        default=c_double(0),
        repr=False,
    )
    curr_veh_CACC_h: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Ego headway space
    # --------------------------------------------------------------------------
    curr_veh_used_distance_headway: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Ego vehicle Dv,v
    # --------------------------------------------------------------------------
    curr_veh_used_rel_vel: c_double = field(
        default=c_double(0),
        repr=False,
    )
    curr_veh_velocity: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Unclear
    # --------------------------------------------------------------------------
    curr_veh_autonomous_operational_warning: c_long = field(
        default=c_long(10),
        repr=False,
    )

    # Max accel/deccel  - Positive value - symmetric
    # --------------------------------------------------------------------------
    curr_veh_platooning_max_acceleration: c_double = field(
        default=c_double(2.0),
        repr=False,
    )

    # Past time info
    # --------------------------------------------------------------------------
    # Speed setpoint -> curr_veh_setspeed
    prev_veh_cc_setpoint: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Return values -> veh_cruisecontrol_acceleration
    prev_veh_cruisecontrol_acceleration: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Ego headway space → curr_veh_used_distance_headway
    prev_veh_distance_headway: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Return values → veh_autonomous_operational_acceleration
    prev_veh_executed_acceleration: c_double = field(
        default=c_double(0),
        repr=False,
    )

    # Return values: These are placeholders, no action required
    # --------------------------------------------------------------------------
    veh_autonomous_operational_acceleration: c_double = field(
        default=c_double(1), repr=False
    )
    veh_autonomous_operational_mixingmode: c_long = field(
        default=c_long(1),
        repr=False,
    )
    veh_autonomous_operational_warning: c_double = field(
        default=c_double(1),
        repr=False,
    )
    veh_cc_setpoint: c_double = field(
        default=c_double(1),
        repr=False,
    )
    veh_cruisecontrol_acceleration: c_double = field(
        default=c_double(1),
        repr=False,
    )
    success: c_int = field(
        default=c_int(0),
        repr=False,
    )

    def __init__(self, path_library: str = DEFAULT_CACC_PATH):
        self._path_library = path_library
        self.load_library(self._path_library)

    def _update_dll(self):
        self.lib.operational_controller(
            self.curr_lead_veh_acceleration,
            self.curr_lead_veh_id,
            self.curr_lead_veh_rel_velocity,
            self.curr_lead_veh_type,
            self.curr_timestep,
            self.curr_ts_length,
            self.curr_veh_id,
            self.curr_veh_setspeed,
            self.curr_veh_type,
            self.curr_veh_controller_in_use,
            self.curr_veh_ACC_h,
            self.curr_veh_CACC_h,
            self.curr_veh_used_distance_headway,
            self.curr_veh_used_rel_vel,
            self.curr_veh_velocity,
            self.curr_veh_autonomous_operational_warning,
            self.curr_veh_platooning_max_acceleration,
            self.prev_veh_cc_setpoint,
            self.prev_veh_cruisecontrol_acceleration,
            self.prev_veh_distance_headway,
            self.prev_veh_executed_acceleration,
            byref(self.veh_autonomous_operational_acceleration),
            byref(self.veh_autonomous_operational_mixingmode),
            byref(self.veh_autonomous_operational_warning),
            byref(self.veh_cc_setpoint),
            byref(self.veh_cruisecontrol_acceleration),
            byref(self.success),
        )
        return self.veh_autonomous_operational_acceleration.value

    def __call__(
        self,
        ego: VehGapCoordinator,
        reference: ReferenceHeadway,
        t: float,
        T: float,
    ):
        """This performs a multiple step call of the operational layer per vehicle.

        Args:
            ego (VehGapCoordinator): Ego vehicle gap coordinator
            reference (ReferenceHeadway): Reference object
            t (float): simulation current time
            T (float): operational time step
            dynamics (AbsDynamics):  Dynamics object to compute vehicle's model

        Returns:
            [type]: [description]
        """

        for i, r in enumerate(reference):
            data_leader, data_ego = ego.get_step_data()
            r_dct = {"t": r[0], "g_cacc": r[1], "g_acc": r[1], "v": r[2]}
            control = self.single_call_control(
                data_leader,
                data_ego,
                r_dct,
                r_dct.get("t", 1),
                T,
            )
            state = np.array(
                [
                    data_ego.get("x"),
                    data_ego.get("v"),
                    data_ego.get("a"),
                ]
            )
            ego._history_state = np.vstack(
                (
                    ego._history_state,
                    ego.ego.dynamics(state, np.array([control])),
                )
            )

    def single_call_control(
        self,
        leader: dict,
        ego: dict,
        r_ego: dict,
        t: float,
        T: float,
    ):
        """Asumes 0 index for lead 1 for follower

        * a: real acceleration
        * x: postition
        * v: speed
        * s: spacing
        * u: control

        * D: delta
        * P: past

        Args:
            leader(dict): vehicle 0 keys, a,x,v,Dv,Pu,Ps
            ego(dict): vehicle 1, keys, a,x,v,Dv,Pu,Ps
            r_ego(dict): reference 1 keys, v,s
            t(float): current time
            T(float): sampling time
        """

        # Past time info

        # Speed setpoint -> curr_veh_setspeed
        self.prev_veh_cc_setpoint = self.curr_veh_setspeed

        # Return values -> veh_cruisecontrol_acceleration
        self.prev_veh_cruisecontrol_acceleration = (
            self.veh_cruisecontrol_acceleration
        )

        # Ego headway space → curr_veh_used_distance_headway
        self.prev_veh_distance_headway = self.curr_veh_used_distance_headway

        # Return values → veh_autonomous_operational_acceleration
        self.prev_veh_executed_acceleration = (
            self.veh_autonomous_operational_acceleration
        )

        # Leader info
        self.curr_lead_veh_acceleration = c_double(leader["a"])
        self.curr_lead_veh_id = c_long(leader["id"])
        self.curr_lead_veh_rel_velocity = c_double(leader["Dv"])
        # self.curr_lead_veh_type=c_long(0)

        # Current time info
        self.curr_timestep = c_double(t)
        self.curr_ts_length = c_double(T)

        ## Ego info
        self.curr_veh_id = c_long(ego["id"])
        # self.curr_veh_type=c_long(1)

        # Speed setpoint
        self.curr_veh_setspeed = c_double(r_ego["v"])

        # Control under use: 1-ACC ,2-CACC
        # self.curr_veh_controller_in_use=c_long(2)

        # Setpoint timegap headways
        self.curr_veh_ACC_h = c_double(r_ego["g_acc"])
        self.curr_veh_CACC_h = c_double(r_ego["g_cacc"])

        # Ego headway space
        self.curr_veh_used_distance_headway = c_double(leader["x"] - ego["x"])

        # Ego vehicle Dv,v
        self.curr_veh_used_rel_vel = c_double(leader["v"] - ego["v"])
        self.curr_veh_velocity = c_double(ego["v"])

        # Unclear
        # self.curr_veh_autonomous_operational_warning

        # Max accel/deccel  - Positive value - symmetric
        # self.curr_veh_platooning_max_acceleration

        return self._update_dll()

    def update_value(self, **kwargs):
        """Update values to compute control"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def load_library(self, path_library):
        """Loads the control library into the controller"""
        self.lib = cdll.LoadLibrary(path_library)


if __name__ == "__main__":
    c = CACC()
