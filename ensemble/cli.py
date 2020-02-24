""" 
    Command Line Interface 
    Scenario launcher for ENSEMBLE simulations

"""

import sys
import click
import typing

from .ensemble import launch_simulation, check_scenario_consistancy

# ------------------------------ Configurator ----------------------------------
class Configurator(object):
    """ 
        This class stores some simulation configurations. 
    """

    def __init__(self, verbose: bool = False) -> None:
        import platform

        self.verbose = verbose
        self.platform = platform.system()
        self.simulation_platform = ""
        self.scenario_files = []
        self.library_path = []

    def set_simulation_platform(self, simulation_platform: str = "") -> None:
        """ A simpler setter for the simulation platform based on OS

        :param simulation_platform: "symuvia" or "vissim", defaults to ""
        :type simulation_platform: str, optional
        """
        if simulation_platform:
            self.simulation_platform = simulation_platform
            return
        dct_simp = {
            "Darwin": "symuvia",
            "Linux": "symuvia",
            "Windows": "vissim",
        }
        self.simulation_platform = dct_simp.get(self.platform, "")
        return


pass_config = click.make_pass_decorator(Configurator)

# ------------------------------ CLI interface ---------------------------------


@click.group()
@click.option("--verbose", is_flag=True)
@click.option("--platform", default="", help="'symuvia' or 'vissim'")
@click.pass_context
def main(ctx, verbose: bool, platform: str) -> int:
    """Scenario launcher for ENSEMBLE simulations"""
    ctx.obj = Configurator(verbose)
    ctx.obj.set_simulation_platform(platform)
    if ctx.obj.verbose:
        click.echo(
            """ENSEMBLE Platooning

               Platform for Simulation of Multibrand Truck Platooning
            """
        )
        click.echo(
            """See click documentation at:

            """
        )
    return 0


# Launch command
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
@click.option("--check", default=False, help="Enable check flag")
@pass_config
def launch(
    config: Configurator, scenario: str, library: str, check: bool
) -> None:
    """ Launches an escenario for a specific platform 
    """
    click.echo(
        "Launching Scenario on platform: "
        + click.style((f"{config.platform}"), fg="green")
    )

    # Update configurator
    config.update_values(library_path=library, scenario_files=scenario)

    # Run optional check
    if check:
        check_scenario_consistancy(config)

    launch_simulation(config)


# Check command
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
def check(config: Configurator, scenario: str, library: str) -> None:
    """ Diagnoses files consistancy and simulator availability
    """

    # Update configurator
    config.update_values(library_path=library, scenario_files=scenario)
    return not check_scenario_consistancy(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
