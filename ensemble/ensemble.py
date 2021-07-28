"""
ENSEMBLE Command Line Commands
====================================
Command definitions 
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import click

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.screen import log_in_terminal
from ensemble.tools.checkers import check_scenario_consistency
from ensemble.logic import RuntimeDevice
from ensemble.control.operational.basic_test import runtime_op_layer


def launch_simulation(configurator):
    """ Launches a RuntimeDevice starting from a configurator 

        Args:
            configurator(Configurator): Configurator class

        Example:
            Use the the function from a python package as::
                >>> from ensemble import launch_simulation, Configurator
                >>> c = Configurator() # default arguments
                >>> library = 'path/to/simulator'
                >>> scenarios = ('path/to/scenario',) 
                >>> config.update_values(library_path=library, scenario_files=scenario)
                >>> launch_simulation(configurator)
    """
    log_in_terminal("Initializing scenario ⏱", fg="magenta")

    with RuntimeDevice(configurator) as rt:
        log_in_terminal("Finalizing simulation ⏱", fg="magenta")


def check_consistency(configurator) -> bool:
    """ Checks consistency of the current configurator
    
        Args:
            configurator(Configurator): Configurator class
    """
    # Check only for consistency, others could be added in future
    return check_scenario_consistency(configurator)


def run_operational_runtime():
    """Considers a demonstration scenario to run in the operational layer with components from the framework. The purpose is to test components from the tactical layer"""
    runtime_op_layer(scenario="platoon")
