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

    def test_construct_from_list_dict(self):
        data = [
            {
                "abscissa": 12.374845509246274,
                "acceleration": 0.1817535409600709,
                "distance": 12.375229607561504,
                "vehid": 1,
                "ordinate": 0.09750108760931722,
                "link": 1,
                "vehtype": "100",
                "speed": 57.01563959662845,
                "lane": 1,
            }
        ]

    def test_construct_from_ordered_dict(self):
        data = OrderedDict()
