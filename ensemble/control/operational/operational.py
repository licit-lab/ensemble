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
from ensemble.metaclass.coordinator import AbsSingleGapCoord
from ensemble.metaclass.dynamics import AbsDynamics

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================
TIME_STEP_OP = DCT_RUNTIME_PARAM["sampling_time_operational"]


@dataclass
class CACC(AbsController):
    """Operational layer class  for containing specific library execution

    Args:
        ID(int):
            EGO Vehicle id

        HMI_control_mode (double):
            ACC or CACC to be used, from tactical layer	ACC=1; CACC =2

        HMI_t_headway (double):
            Desired time gap from tactical layer [s]

        HMI_setSpeed (double):
            Desired speed from tactical layer [m/s]

        EGO_lon_velocity (double):
            EGO vehicle longitudinal velocity [m/s]

        EGO_lon_acceleration (double):
            EGO vehicle longitudinal acceleration [m/s^2]

        MIO_dv_limit (Double):
            Front target relative velocity: target velocity – ego velocity [m/s]

        MIO_lon_distance (Double):
            Longitudinal distance gap [m]

        MIO_objectID (double):
                Target ID [int]

        MIO_acceleration (double):
                Leader's actual current acceleration [m/s^2]

        MIO_datamodeA (double):
            Data resource. No target = 0, detected with wifi + radar + camera = 7 (choose either 0 or 7)

        MIO_u_ffA (double):
            Communicated target desired acceleration [m/s^2]
            Acceleration output of the target’s operational layer, not the output of vehicle model.
            Also: Leader's desired acceleration. If leader not platoon vehicle or not leader set value to zero.
    """

    # --------------------------------------------------------------------------
    ID: c_double = field(
        default=c_int(1),
        repr=False,
    )
    HMI_control_mode: c_double = field(
        default=c_double(1),
        repr=False,
    )
    HMI_t_headway: c_double = field(
        default=c_double(1.4),
        repr=False,
    )
    EGO_lon_velocity: c_double = field(
        default=c_double(0),
        repr=False,
    )
    EGO_lon_acceleration: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_dv_limit: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_lon_distance: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_objectID: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_acceleration: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_datamodeA: c_double = field(
        default=c_double(0),
        repr=False,
    )
    MIO_u_ffA: c_double = field(
        default=c_double(0),
        repr=False,
    )
    u_control: c_double = field(
        default=c_double(0),
        repr=False,
    )

    def __init__(self, path_library: str = DEFAULT_CACC_PATH):
        self._path_library = path_library
        self.load_library(self._path_library)

    def _update_dll(self):
        self.lib.combined_acc_cacc_dll(
            self.ID,
            self.HMI_control_mode,
            self.HMI_t_headway,
            self.HMI_setSpeed,
            self.EGO_lon_velocity,
            self.EGO_lon_acceleration,
            self.MIO_dv_limit,
            self.MIO_lon_distance,
            self.MIO_objectID,
            self.MIO_acceleration,
            self.MIO_datamodeA,
            self.MIO_u_ffA,
            byref(self.u_control),
        )
        return self.u_control.value

    def __call__(
        self,
        vgc: AbsSingleGapCoord,
        reference: ReferenceHeadway,
        t: float,
        T: float,
    ):
        """This performs a multiple step call of the operational layer per vehicle.

        Args:
            vgc (AbsSingleGapCoord): vgc vehicle gap coordinator
            reference (ReferenceHeadway): Reference object
            t (float): simulation current time
            T (float): operational time step
            dynamics (AbsDynamics):  Dynamics object to compute vehicle's model

        Returns:
            [type]: [description]
        """

        for _, r in enumerate(reference):
            data_leader, data_ego = vgc.get_step_data()
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
            vgc.history_state = vgc.ego.dynamics(state, np.array([control]))
            vgc.history_control = np.array([control])

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
        self.ID = c_int(ego["id"])
        self.HMI_control_mode = c_double(2)
        if self.HMI_control_mode == c_double(2):
            self.HMI_t_headway = c_double(r_ego["g_cacc"])
        elif self.HMI_control_mode == c_double(1):
            self.HMI_t_headway = c_double(r_ego["g_acc"])
        self.HMI_setSpeed = c_double(r_ego["v"])
        self.EGO_lon_velocity = c_double(ego["v"])
        self.EGO_lon_acceleration = c_double(ego["a"])
        self.MIO_dv_limit = c_double(leader["v"] - ego["v"])
        self.MIO_lon_distance = c_double(leader["x"] - ego["x"])
        self.MIO_objectID = c_double(leader["id"])
        self.MIO_acceleration = c_double(leader["a"])
        self.MIO_datamodeA = c_double(7)
        self.MIO_u_ffA = c_double(leader["u"])
        self.u_control = c_double(0)
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
