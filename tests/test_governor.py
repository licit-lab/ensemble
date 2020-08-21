"""
    Unit tests for the Multibrand Platooning Registry 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import unittest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.control.governor import MultiBrandPlatoonRegistry
from ensemble.component.vehicles import Vehicle

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


class TestConstruction(unittest.TestCase):
    def test_construct_empty(self):
        s = MultiBrandPlatoonRegistry()
