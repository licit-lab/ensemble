"""
    Main module to control simulation in each one of the
    simulation platforms

"""
import click

from ensemble.handler_symuvia.new_file import my_func
from ensemble.handler_vissim.start_vissim import another_function

# Config files


def launch_simulation(configurator) -> None:
    """ Selector and simulation specific launcher """
    click.echo("Initializing platform")


def configure_scenario():
    """
    """
    pass


def check_scenario_consistancy(configurator) -> bool:
    """ Determine the consistancy of files and libraries where indicated"""
    click.echo("Checking consistancy of files")
