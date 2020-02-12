""" 
    Command Line Interface 
    Scenario launcher for ENSEMBLE simulations

"""

import sys
import click

# from .ensemble import launch_simulation():


@click.group()
def main(args=None):
    """Scenario launcher for ENSEMBLE simulations"""
    click.echo(
        "Replace this message by putting your code into " "ensemble.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@main.command()
@click.option(
    "-s", "--scenario", default="", help="Scenario file under analysis."
)
@click.option("-l", "--library", default="", help="Full path towards library.")
def launch(scenario, library_path):
    """ Launch a given scenario in a specific platform 
    """
    click.echo("Launching Scenario")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
