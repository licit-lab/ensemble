"""
    Unit tests for symupy.utils.configurator 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import ensemble.tools.constants as CT
from ensemble.configurator import Configurator
from ensemble.handler.symuvia import SymuviaConfigurator


# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    uname = platform.system()
    key = ("symuvia", uname)
    return CT.DCT_DEFAULT_PATHS[key]


def test_configurator_cli():
    Configurator(verbose=True, info=True)


def test_default_configurator_constructor(symuvia_library_path):
    config = SymuviaConfigurator()
    # Checks default parameters
    assert len(config.buffer_string.raw) == CT.BUFFER_STRING
    assert config.library_path == symuvia_library_path
    assert config.trace_flow == CT.TRACE_FLOW
    assert config.total_steps == CT.TOTAL_SIMULATION_STEPS
    assert config.step_launch_mode == CT.LAUNCH_MODE
