""" This module contains functions to check 

:raises click.Abort: Raise errors when values are not satisfied
:raises EnsembleAPIWarning: [description]
:raises click.UsageError: [description]
:return: [description]
:rtype: [type]
"""

import click
from pathlib import Path


def check_library_path(configurator) -> bool:
    """ Returns true if platform is available
    """
    click.echo("Looking for library path: " + click.style(f"{configurator.library_path}", fg="blue"))
    if Path(configurator.library_path).exists():
        return True

    click.echo("Given Library Path: " + click.style(f"{configurator.library_path}", fg="red") + "does not exist")
    raise click.Abort()
    return False


def check_scenario_path(configurator) -> bool:
    """ Returns true if all scenario file(s) are available
    """
    click.echo("Looking for scenario files: " + click.style(f"{configurator.scenario_files}", fg="blue"))
    if configurator.scenario_files:
        for file in configurator.scenario_files:
            if Path(configurator.library_path).exists():
                scenario = True
            else:
                scenario = False
                # raise EnsembleAPIWarning(
                #     f"Scenario File : {configurator.file}. Not Found "
                # )
        return scenario
    raise click.UsageError("Scenario file(s) is an empty list")

    return False


def check_scenario_consistency(configurator) -> bool:
    """ Determine the consistency of files and libraries where indicated"""

    # Print info
    click.echo(click.style("Checking consistency of files", fg="blue", bold=True))

    # Check for Library
    platform = check_library_path(configurator)

    # Check for scenarios
    scenario = check_scenario_path(configurator)

    return platform * scenario
