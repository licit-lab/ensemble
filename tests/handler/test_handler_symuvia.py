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

from ensemble.handler.symuvia import (
    SymuviaConfigurator,
    SymuviaConnector,
    SymuviaScenario,
)
import ensemble.tools.constants as CT

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]


def test_configurator_constructor(symuvia_library_path):
    config = SymuviaConfigurator()
    assert len(config.buffer_string.raw) == CT.BUFFER_STRING
    assert config.library_path == symuvia_library_path
    assert config.trace_flow == CT.TRACE_FLOW
    assert config.total_steps == CT.TOTAL_SIMULATION_STEPS
    assert config.step_launch_mode == CT.LAUNCH_MODE


def test_connector_constructor(symuvia_library_path):
    connector = SymuviaConnector(library_path=symuvia_library_path)
    assert connector.library_path == symuvia_library_path
    assert connector.trace_flow == CT.TRACE_FLOW
    assert connector.total_steps == CT.TOTAL_SIMULATION_STEPS
    assert connector.step_launch_mode == CT.LAUNCH_MODE
