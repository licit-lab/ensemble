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
from numpy.testing import assert_array_equal

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.dynamics import dynamic_2nd_ego, dynamic_3rd_ego

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
