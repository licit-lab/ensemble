"""
Unit testing
============

    Note:
        Tests for `ensemble.control.operational.reference`

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

from ensemble.control.operational.reference import ReferenceHeadway
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


def test_splitting():
    r = ReferenceHeadway()
    r.create_time_gap_hwy(Splitting())
    assert pytest.approx(r.reference[-1], 3 * 1.4)


def test_joining():
    r = ReferenceHeadway(gap0=2)
    r.create_time_gap_hwy(Joining())
    assert r.reference[-1] == 1.4
