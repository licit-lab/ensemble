"""
    Main module to control simulation in each one of the
    simulation platforms

"""
import click

from ensemble.handler_symuvia.new_file import my_func
from ensemble.handler_vissim.start_vissim import another_function

from pathlib import Path

# Config files

def check_library_path(configurator) -> bool:
    """ Returns true if platform is available
    """
    click.echo(
        "Looking for library path: "
        + click.style(f"{configurator.library_path}", fg="blue")
    )
    if Path(configurator.library_path).exists():
        return True

    click.echo(
        "Given Library Path: "
        + click.style(f"{configurator.library_path}", fg="red")
        + "does not exist"
    )
    raise click.Abort()
    return False


def check_scenario_path(configurator) -> bool:
    """ Returns true if all scenario file(s) are available
    """
    click.echo(
        "Looking for scenario files: "
        + click.style(f"{configurator.scenario_files}", fg="blue")
    )
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


def check_scenario_consistancy(configurator) -> bool:
    """ Determine the consistancy of files and libraries where indicated"""

    # Initial check
    click.echo(
        click.style("Checking consistancy of files", fg="blue", bold=True)
    )

    click.echo()
    # Check for Library
    platform = check_library_path(configurator)

    # Check for scenarios
    scenario = check_scenario_path(configurator)

    return platform * scenario


def launch_simulation(configurator) -> None:
    """ Selector and simulation specific launcher """
    click.echo("Initializing platform")


def configure_scenario():
    """
    """
    pass
