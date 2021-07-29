""" 
Check module 
====================================
This module contains functions to check 
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import click
from pathlib import Path

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.exceptions import EnsembleAPIWarning
from ensemble.tools.screen import (
    log_success,
    log_verify,
    log_warning,
    log_error,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

LINE_SEP = "*".join(["*"] * 40)


def check_library_path(library_path: str, simulation_platform: str):
    """Returns true if platform is available"""

    log_verify(
        LINE_SEP,
        f"Looking for library path:",
        f"{library_path}",
        LINE_SEP,
    )

    if simulation_platform == "symuvia":
        if not Path(library_path).exists():
            log_error(f"\tGiven Library Path: {library_path} does not exist")
            return False
    else:
        log_warning(
            "\tPlatform and path:",
            "\t{simulation_platform} -- {library_path}",
            " were not verified.",
        )
    # Check Path existance for symuvia

    if simulation_platform == "symuvia" and Path(library_path).exists():
        log_success(f"Platform Found:", f"\t{library_path}")
        return True
    elif simulation_platform == "symuvia":
        log_error("Given Library Path:", f"\t{library_path}", "does not exist")
    else:
        # Tests for Vissim should go here
        log_warning(
            "Platform and path:",
            f"\t{simulation_platform} -- {library_path}",
            "were not verified.",
        )
        return True


def check_scenario_path(scenario_files: tuple) -> bool:
    """Returns true if all scenario file(s) are available"""
    log_verify(
        LINE_SEP,
        f"Looking for scenario files: ",
        f"{scenario_files}",
        LINE_SEP,
    )

    scenario = True
    temp = False
    if scenario_files:
        for file in scenario_files:
            if Path(file).exists():
                log_success(f"\tInput File: {file} Found")
                temp = True
            else:
                temp = False
                EnsembleAPIWarning(f"Input File: {file}. Not Found")
        return scenario and temp
    raise click.UsageError("\tScenario file(s) is an empty list")


def check_scenario_consistency(configurator) -> bool:
    """ Determine the consistency of files and libraries where indicated"""

    # Print info
    log_verify(
        LINE_SEP,
        "Checking consistency of files",
        LINE_SEP,
    )

    # Check for Library
    platform = check_library_path(
        configurator.library_path, configurator.simulation_platform
    )

    # Check for scenarios
    scenario = check_scenario_path(configurator.scenario_files)

    return bool(platform * scenario)
