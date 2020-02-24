""" 
    Command Line Interface 
    Scenario launcher for ENSEMBLE simulations

"""

import sys
import click
import typing

from .ensemble import launch_simulation, check_scenario_consistancy

# ------------------------------ Configurator ----------------------------------

# Constant values

# Default simulator per platform

DCT_SIMULATORS = {
    "Darwin": "symuvia",
    "Linux": "symuvia",
    "Windows": "vissim",
}

# Default path simulators

DCT_DEFAULT_PATHS = {
    (
        "symuvia",
        "Darwin",
    ): "/Users/ladino/Documents/03-Code/02-Python/libraries/symupy/lib/osx-64/libSymuVia.dylib",
    ("symuvia", "Linux"): "/home/build-symuvia/build/symuvia/libSymuVia.dylib",
    ("visim", "Windows"): "Vissim.Vissim-64.10",
}


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

        self.simulation_platform = DCT_SIMULATORS.get(self.platform, "")

        click.echo(
            click.style(
                f"Setting default simulation platform platform {(self.simulation_platform, self.platform)}",
                fg="yellow",
            )
        )

        self.library_path = DCT_DEFAULT_PATHS.get(
            (self.simulation_platform, self.platform)
        )

        click.echo(
            click.style(
                f"Simulator path set to default value:\n \t {self.library_path}",
                fg="green",
            )
        )
        return

    def update_values(self, **kwargs) -> None:
        """ Configurator updater, pass a with keyword arguments to update
        """

        if kwargs.get("library_path"):

            self.library_path = kwargs.get("library_path", self.library_path)

            click.echo(
                click.style(
                    f"Setting new library path to user input:\n \t{self.library_path}",
                    fg="yellow",
                )
            )

        if kwargs.get("scenario_files"):
            self.scenario_files = kwargs.get(
                "scenario_files", self.scenario_files
            )

            click.echo(
                click.style(
                    f"Setting new scenario file(s) path to user input:  {self.library_path}",
                    fg="yellow",
                )
            )


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
