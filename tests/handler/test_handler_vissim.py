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

from ensemble.handler.vissim import (
    VissimConfigurator,
    VissimConnector,
    VissimScenario,
)

import ensemble.tools.constants as CT

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================
@pytest.fixture
def vissim_library_path():
    return CT.DCT_DEFAULT_PATHS[("vissim", platform.system())]


def test_configurator_constructor(vissim_library_path):
    config = VissimConfigurator()
    assert True
    assert config.library_path == vissim_library_path


def test_connector_constructor(vissim_library_path):
    try:
        connector = VissimConnector(library_path=vissim_library_path)
        assert connector.library_path == vissim_library_path
    except:
        with pytest.raises(Exception) as e_info:
            connector = VissimConnector(library_path=vissim_library_path)
