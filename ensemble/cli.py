""" 
ENSEMBLE Command Line Interface
====================================
Scenario launcher for ENSEMBLE simulations
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import sys
import click
import typing

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import ensemble.tools.constants as ct
from .ensemble import launch_simulation, check_consistency
from .configurator import Configurator

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


pass_config = click.make_pass_decorator(Configurator)

help_text = """ENSEMBLE Platooning

Platform for Simulation of Multibrand Truck Platooning

This is a Command Line Interface to simulate multibrand truck platooning 
in a traffic live environment, with the aim to examine impact on traffic 
flow.

Please visit: https://platooningensemble.eu for more information.

See click documentation at:

file://ensemble/docs/_build/html/index.html

"""
# ------------------------------ CLI interface --------------------------------


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Increase verbosity.")
@click.option("-i", "--info", is_flag=True, help="Prints additional information")
@click.option("-p", "--platform", default="", help="'symuvia' or 'vissim'")
@click.pass_context
def main(ctx, verbose: bool, info: str, platform: str) -> int:
    """Scenario launcher for ENSEMBLE simulations"""
    ctx.obj = Configurator(verbose=verbose, info=info)
    ctx.obj.set_simulation_platform(platform)
    if ctx.obj.verbose:
        click.echo(
            click.style(
                help_text,
                fg="green",
            )
        )
    return 0


# ------------------------------ Launch command--------------------------------


@main.command()
@click.option(
    "-s",
    "--scenario",
    default="",
    multiple=True,
    help="Scenario file(s) under analysis.",
)
@click.option(
    "-l", "--library", default="", type=str, help="Full path towards library."
)
@click.option("--check", is_flag=True, help="Enable check flag")
@click.option("--steps", default=0, help="Simulates n time steps")
@pass_config
def launch(
    config: Configurator, scenario: str, library: str, check: bool, steps: int
) -> None:
    """Launches an escenario for a specific platform"""
    click.echo(
        "Launching Scenario on platform: "
        + click.style((f"{config.platform}"), fg="green")
    )

    # Update configurator
    config.update_values(
        library_path=library, scenario_files=scenario, sim_steps=steps
    )

    # Run optional check
    if check:
        check_consistency(config)

    launch_simulation(config)


# ----------------------------- Check command----------------------------------


@main.command()
@click.option(
    "-s",
    "--scenario",
    default="",
    multiple=True,
    help="Scenario file under analysis.",
)
@click.option(
    "-l", "--library", default="", type=str, help="Full path towards library."
)
@pass_config
def check(config: Configurator, scenario: str, library: str) -> bool:
    """Diagnoses files consistancy and simulator availability"""

    # Update configurator
    config.update_values(library_path=library, scenario_files=scenario)

    return check_consistency(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
