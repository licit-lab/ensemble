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
from dataclasses import dataclass

from symupy.utils.constants import TIME_STEP_OP


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


from ensemble.metaclass.dynamics import AbsDynamics
from ensemble.tools import constants as ct
from ctypes import cdll, c_double, c_int8, c_uint8, c_bool, byref
from ensemble.tools.constants import (
    DEFAULT_TRUCK_PATH,
    DCT_RUNTIME_PARAM,
    DCT_SIMULATION_INFO,
    ENGINE_CONSTANT,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


TIME_STEP = DCT_RUNTIME_PARAM["sampling_time_operational"]
TAU = ENGINE_CONSTANT


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

    position: float = 0
    acceleration: float = 0
    speed: float = 0

    def __init__(self, path_library: str = DEFAULT_TRUCK_PATH):
        self._path_library = path_library
        self.load_library(self._path_library)

        self.a = c_double(0)
        self.b = c_double(0)
        self.c = c_double(0)
        self.d = c_double(0)
        self.e = c_double(0)
        self.f = c_double(0)

        self.h = c_double(0)
        self.i = c_double(0)
        self.j = c_double(0)
        self.k = c_double(0)
        self.l = c_double(0)
        self.m = c_double(0)
        self.n = c_double(0)
        self.o = c_double(0)
        self.p = c_double(0)
        self.q = c_double(0)
        self.r = c_double(0)
        self.s = c_int8(0)
        self.t = c_int8(0)
        self.u = c_uint8(0)
        self.v = c_uint8(0)
        self.w = c_bool(False)
        self.y = c_bool(False)

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
        acc = self.lib.TruckDynamics_dll(
            c_double(external_acc),
            byref(self.a),
            byref(self.b),
            byref(self.c),
            byref(self.d),
            byref(self.e),
            byref(self.f),
            byref(self.h),  ####
            byref(self.i),
            byref(self.j),
            byref(self.k),
            byref(self.l),
            byref(self.m),
            byref(self.n),
            byref(self.o),
            byref(self.p),
            byref(self.q),
            byref(self.r),
            byref(self.s),
            byref(self.t),
            byref(self.u),
            byref(self.v),
            byref(self.w),
            byref(self.y),
        )
        return np.array((acc,))

    def __call__(self, state: np.ndarray, control: np.ndarray) -> np.ndarray:
        """Computes the dynamics passing through the truck

        Args:
            state (np.ndarray): Truck state @k (position, speed)
            control (np.ndarray):

        Returns:
            np.ndarray:
        """

        acc = self.getAcceleration(control[:1])
        return dynamic_2nd_ego(state, acc)


@dataclass
class RegularDynamics(AbsDynamics):
    def __init__(self):
        pass

    @property
    def T(self):
        return TIME_STEP

    def __call__(self, state: np.ndarray, control: np.ndarray) -> np.ndarray:
        return dynamic_3rd_ego(state, control)


class PlatoonDynamics:
    """Potential class for handling vector state for platoons"""


if __name__ == "__main__":
    import os

    truck_path = os.path.join(
        os.getcwd(), "..", "libs", "darwin", "truckDynamics.dylib"
    )
    t = TruckDynamics(truck_path)
