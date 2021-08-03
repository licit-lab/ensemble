"""
Dynamics Model
==============

This module contains a set of models to explain the truck dynamics. The way in which dynamics are regularly described are: 

.. math::
   x_{k+1} = f(x_k)

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import typing
import numpy as np
from dataclasses import dataclass, field
from ctypes import c_double, c_int, byref


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


from ensemble.metaclass.dynamics import AbsDynamics
from ensemble.tools.exceptions import EnsembleAPIError
from ensemble.tools.screen import log_warning
from ensemble.tools import constants as ct
from ctypes import cdll, c_double, c_int8, c_uint8, c_bool, byref
from ensemble.tools.constants import (
    DEFAULT_TRUCK_PATH,
    DCT_RUNTIME_PARAM,
    DCT_TRUCK_PARAM,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

TIME_STEP = DCT_RUNTIME_PARAM["sampling_time_operational"]
TAU = DCT_TRUCK_PARAM["engineTau"]
LENGTH = DCT_TRUCK_PARAM["length"]
WIDTH = DCT_TRUCK_PARAM["width"]
MASS = DCT_TRUCK_PARAM["mass"]
INTERAXES = DCT_TRUCK_PARAM["interAxes"]


def dynamic_3rd_ego(state: np.ndarray, control: np.ndarray) -> np.ndarray:
    """Update vehicle state in 3rd order dynamics

    Args:
        state (np.ndarray): 3d-array @ k [position;speed;acceleration]
        control (np.ndarray): 1d-array [control]

    Returns:
        np.ndarray: [3d-array] @ k+1 [position;speed;acceleration]
    """
    K_a = TIME_STEP / TAU
    A = np.array(
        [
            [1, TIME_STEP, 0],
            [0, 1, TIME_STEP],
            [0, 0, (1 - K_a)],
        ]
    )
    B = np.array([[0], [0], [K_a]])
    return A @ state[:3] + B @ control[:1]


def dynamic_2nd_ego(state: np.ndarray, control: np.ndarray) -> np.ndarray:
    """Update vehicle state in 2nd order dynamics

    Args:
        state (np.ndarray): 2d-array @ k [position;speed]
        control (np.ndarray): 1d-array [control]

    Returns:
        np.ndarray: [3d-array] @ k+1 [position;speed]
    """
    A = np.array([[1, TIME_STEP], [0, 1]])
    B = np.array([[0], [TIME_STEP]])
    return A @ state[:2] + B @ control[:1]


@dataclass
class TruckDynamics(AbsDynamics):
    """External truck model"""

    vehid: c_int = field(repr=True)
    x: c_double = field(repr=True)
    a: c_double = field(repr=True)
    v: c_double = field(repr=True)
    width: c_double = field(default=c_double(WIDTH), repr=False)
    length: c_double = field(default=c_double(LENGTH), repr=False)
    interAxes: c_double = field(default=c_double(INTERAXES), repr=False)
    mass: c_double = field(default=c_double(MASS), repr=False)
    library: str = field(default=DEFAULT_TRUCK_PATH, repr=False)

    def __init__(self, vehid: int, x: float, v: float, a: float):
        self.vehid = c_int(vehid)
        self.x = c_double(x)
        self.v = c_double(v)
        self.a = c_double(a)
        self.load_library(self.library)

    def load_library(self, path_library):
        """Loads the truck library into the class"""
        self.lib = cdll.LoadLibrary(path_library)

    @property
    def T(self):
        return TIME_STEP

    def getAcceleration(self, external_acc: float) -> np.ndarray:
        """Computes truck acceleration

        Args:
            external_acc (float): CACC/ACC commanded control

        Returns:
            np.ndarray: Truck acceleration for state computation.
        """
        self.lib.TruckDynamics_dll(
            self.vehid,
            c_double(external_acc),
            byref(self.x),
            byref(self.v),
            byref(self.a),
            byref(self.interAxes),
            byref(self.length),
            byref(self.width),
            byref(self.mass),
        )
        return np.array([self.x.value, self.v.value, self.a.value])

    def __call__(self, state: np.ndarray, control: np.ndarray) -> np.ndarray:
        """Computes the dynamics passing through the truck

        Args:
            state (np.ndarray): Truck state @k (position, speed)
            control (np.ndarray):

        Returns:
            np.ndarray:
        """

        self.lib.TruckDynamics_dll(
            self.vehid,
            c_double(control[-1]),
            byref(self.x),
            byref(self.v),
            byref(self.a),
            byref(self.interAxes),
            byref(self.length),
            byref(self.width),
            byref(self.mass),
        )
        return np.array([self.x.value, self.v.value, self.a.value])


@dataclass
class RegularDynamics(AbsDynamics):
    def __init__(self):
        pass

    @property
    def T(self):
        return TIME_STEP

    def __call__(self, state: np.ndarray, control: np.ndarray) -> np.ndarray:
        return dynamic_3rd_ego(state, control)


@dataclass
class SampleDynamics(AbsDynamics):
    @property
    def T(self):
        pass

    def __call__(self, state: np.ndarray, control: np.ndarray):
        log_warning("Calling non-existing dynamics")
        raise EnsembleAPIError(
            "Trying to call non existent dynamics. Try defining `RegularDynamics` or `TruckDynamics` from the dynamics module"
        )


class PlatoonDynamics:
    """Potential class for handling vector state for platoons"""


if __name__ == "__main__":
    # Run from base folder
    import os

    truck_path = os.path.join(
        os.getcwd(),
        "ensemble",
        "libs",
        "darwin",
        "truckDynamics.dylib",
    )
    t = TruckDynamics(vehid=0, x=0, a=0, v=25)
