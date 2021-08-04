"""
Unit testing
============

    Note:
        Tests for `ensemble.component.dynamics`

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from matplotlib import pyplot as plt
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_almost_equal

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.dynamics import (
    dynamic_2nd_ego,
    dynamic_3rd_ego,
    TruckDynamics,
)

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


def test_dynamic_2nd_ego():
    x = np.array((0, 25))
    u = np.array((0.1,))
    x_plus = dynamic_2nd_ego(x, u)
    assert type(x_plus) == np.ndarray
    assert_array_equal(x_plus, np.array((2.5, 25.01)))


def test_dynamic_3rd_ego():
    x = np.array((0, 25, 0))
    u = np.array((0.1,))
    x_plus = dynamic_3rd_ego(x, u)
    assert type(x_plus) == np.ndarray
    assert_array_equal(x_plus, np.array((2.5, 25.0, 0.05)))


def test_dynamics_truck_single_step():
    t = TruckDynamics(vehid=0, x=0, a=0, v=25)
    state = t(np.array([]), np.array([1]))
    assert_almost_equal(
        state,
        np.array([2.227778, 24.722222, 0.0]),
        decimal=6,
    )


def test_dynamics_truck_300_step():
    t = TruckDynamics(vehid=0, x=0, a=0, v=25)
    full_state = np.empty((3,))
    state = np.empty((3,))
    full_time = []
    for time in np.arange(0, 30, 0.1):
        state = t(np.array([]), np.array([0.5]))
        full_state = np.vstack((full_state, state))
        full_time.append(time)

    f, a = plt.subplots(1, 3, figsize=(15, 5))
    a[0].plot(full_time, full_state[1:, 1])
    a[0].set_xlabel("Time [s]")
    a[0].set_ylabel("Speed [m/s]")
    a[0].grid(True)

    a[1].plot(full_time, full_state[1:, 2])
    a[1].set_xlabel("Time [s]")
    a[1].set_ylabel("Acceleration [m/s2]")
    a[1].grid(True)

    a[2].plot(full_time, full_state[1:, 0])
    a[2].set_xlabel("Time [s]")
    a[2].set_ylabel("Position [m]")
    a[2].grid(True)

    # plt.show()

    assert_almost_equal(
        full_state[-1],
        np.array([7.410787e02, 2.472222e01, 2.742790e-01]),
        decimal=4,
    )


def test_dynamics_truck_300_step():
    t = TruckDynamics(vehid=0, x=0, a=0, v=0)
    full_state = np.empty((3,))
    state = np.empty((3,))
    full_time = []
    for time in np.arange(0, 30, 0.1):
        state = t(np.array([]), np.array([0.5]))
        full_state = np.vstack((full_state, state))
        full_time.append(time)

    f, a = plt.subplots(1, 3, figsize=(15, 5))
    a[0].plot(full_time, full_state[1:, 1])
    a[0].set_xlabel("Time [s]")
    a[0].set_ylabel("Speed [m/s]")
    a[0].grid(True)

    a[1].plot(full_time, full_state[1:, 2])
    a[1].set_xlabel("Time [s]")
    a[1].set_ylabel("Acceleration [m/s2]")
    a[1].grid(True)

    a[2].plot(full_time, full_state[1:, 0])
    a[2].set_xlabel("Time [s]")
    a[2].set_ylabel("Position [m]")
    a[2].grid(True)

    # plt.show()

    assert_almost_equal(
        full_state[-1],
        np.array([201.1149, 13.3752, 0.5]),
        decimal=4,
    )
