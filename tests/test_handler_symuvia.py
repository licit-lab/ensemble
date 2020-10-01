"""
    Unittesting for ensemble.handle module 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import unittest
import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.handler.symuvia import SymuviaConfigurator, SymuviaConnector, SymuviaScenario
import ensemble.tools.constants as CT

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================

@pytest.fixture
def symuvia_library_path():
    return CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]

def test_configurator_constructor(symuvia_library_path):
    config = SymuviaConfigurator()
    assert config.bufferString == CT.BUFFER_STRING
    assert config.libraryPath == symuvia_library_path
    assert config.stepLaunchMode == CT.LAUNCH_MODE