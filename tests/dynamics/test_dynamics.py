"""
Unit testing
============

    Note:
        Tests for `ensemble.component.dynamics`

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

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
