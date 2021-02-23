"""
    Unit tests for symupy.utils.constants 

    Tests here are just to verify that solution of the platform is the right one and verify the existance of the platform in the system
    
    Important: Define SYMUVIALIB as a an environment variable
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


import os
from pathlib import Path
import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.constants import DCT_DEFAULT_PATHS

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    uname = platform.system()
    key = ("symuvia", uname)
    return DCT_DEFAULT_PATHS[key]


def test_detection_symupy(symuvia_library_path):
    assert Path(symuvia_library_path).exists() == True
