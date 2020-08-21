"""
    Unit tests for the Vehicle object within the ENSEMBLE API     
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import unittest
from collections import OrderedDict

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehicles import Vehicle

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


class TestConstruction(unittest.TestCase):
    def test_construct_empty(self):
        v = Vehicle()

    def test_construct_from_regular_dict(self):
        data = {
            "abscissa": 0.0,
            "acceleration": 0.0,
            "distance": 0.0,
            "vehid": 0,
            "ordinate": 0.0,
            "link": "",
            "vehtype": "",
            "speed": 0.0,
            "lane": 0,
            "elevation": 0.0,
        }

        v = Vehicle(**data)

    def test_construct_from_ordered_dict(self):
        data = OrderedDict()
