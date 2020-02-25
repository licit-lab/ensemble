""" 
    Command Line Interface 
    Scenario launcher for ENSEMBLE simulations

"""

import sys
import click
import typing

import ensemble.tools.constants as ct
from .ensemble import launch_simulation
from ensemble.tools.checkers import check_scenario_consistency

# ------------------------------ Configurator ------------------------------------------------------


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

        click.echo(click.style("Solving platform ", fg="blue", bold=True))

        self.simulation_platform = ct.DCT_SIMULATORS.get(self.platform, "")

        if self.verbose:
            click.echo(
                click.style(
                    f"Setting default simulation platform platform {(self.  simulation_platform, self.platform)}",
                    fg="yellow",
                )
            )

        self.library_path = ct.DCT_DEFAULT_PATHS.get((self.simulation_platform, self.platform))

        click.echo(click.style(f"Simulator path set to default value:\n \t {self.library_path}", fg="green",))
        return

    def update_values(self, **kwargs) -> None:
        """ Configurator updater, pass a with keyword arguments to update
        """

        if kwargs.get("library_path"):

            self.library_path = kwargs.get("library_path", self.library_path)

            click.echo(click.style(f"Setting new library path to user input:\n \t{self.library_path}", fg="yellow",))

        if kwargs.get("scenario_files"):
            self.scenario_files = kwargs.get("scenario_files", self.scenario_files)

            click.echo(
                click.style(f"Setting new scenario file(s) path to user input:  {self.library_path}", fg="yellow",)
            )


pass_config = click.make_pass_decorator(Configurator)

# ------------------------------ CLI interface -----------------------------------------------------


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


# ------------------------------ Launch command-----------------------------------------------------


@main.command()
@click.option("-s", "--scenario", default="", multiple=True, help="Scenario file(s) under analysis.")
@click.option("-l", "--library", default="", type=str, help="Full path towards library.")
@click.option("--check", default=False, help="Enable check flag")
@pass_config
def launch(config: Configurator, scenario: str, library: str, check: bool) -> None:
    """ Launches an escenario for a specific platform 
    """
    click.echo("Launching Scenario on platform: " + click.style((f"{config.platform}"), fg="green"))

    # Update configurator
    config.update_values(library_path=library, scenario_files=scenario)

    # Run optional check
    if check:
        check_scenario_consistency(config)

    launch_simulation(config)


# ------------------------------------------------- Check command-------------------------------------------------------


@main.command()
@click.option("-s", "--scenario", default="", multiple=True, help="Scenario file under analysis.")
@click.option("-l", "--library", default="", type=str, help="Full path towards library.")
@pass_config
def check(config: Configurator, scenario: str, library: str) -> None:
    """ Diagnoses files consistancy and simulator availability
    """

    # Update configurator
    click.echo(scenario)
    click.echo(library)
    config.update_values(library_path=library, scenario_files=scenario)
    return check_scenario_consistancy(config)


# ------------------------------------------------- Main command--------------------------------------------------------


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
