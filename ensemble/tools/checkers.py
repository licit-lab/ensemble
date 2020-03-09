""" This module contains functions to check 

:raises click.Abort: Raise errors when values are not satisfied
:raises EnsembleAPIWarning: [description]
:raises click.UsageError: [description]
:return: [description]
:rtype: [type]
"""

from ensemble.tools.exceptions import EnsembleAPIWarning

import click
from pathlib import Path


def check_library_path(configurator) -> bool:
    """ Returns true if platform is available
    """
    click.echo("Looking for library path: " + click.style(f"{configurator.library_path}", fg="blue"))

    # Check Path existance for symuvia
    if configurator.simulation_platform == "symuvia" and Path(configurator.library_path).exists():
        return True
    elif configurator.simulation_platform == "symuvia":
        click.echo("Given Library Path: " + click.style(f"{configurator.library_path}", fg="red") + " does not exist")
    else:
        click.echo(
            f"Platform and path: "
            + click.style(f"{configurator.platform} -- {configurator.library_path}", fg="red",)
            + " were not verified."
        )
        return True


def check_scenario_path(configurator) -> bool:
    """ Returns true if all scenario file(s) are available
    """
    click.echo("Looking for scenario files: " + click.style(f"{configurator.scenario_files}", fg="blue"))
    scenario = True
    if configurator.scenario_files:
        for file in configurator.scenario_files:
            if Path(file).exists():
                click.echo("Input File: " + click.style(f"{file} Found", fg="green", bold=True))
                temp = True
            else:
                temp = False
                EnsembleAPIWarning(f"Input File: {file}. Not Found ")
        return scenario and temp
    raise click.UsageError("Scenario file(s) is an empty list")


def check_scenario_consistency(configurator) -> bool:
    """ Determine the consistency of files and libraries where indicated"""

    # Print info
    click.echo(click.style("Checking consistency of files", fg="blue", bold=True))

    # Check for Library
    platform = check_library_path(configurator)

    # Check for scenarios
    scenario = check_scenario_path(configurator)

    return platform * scenario
