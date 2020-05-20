"""
    Main module to control simulation in each one of the
    simulation platforms

"""
import click


from ensemble.state import RuntimeDevice


def launch_simulation(configurator) -> None:
    """ Selector and simulation specific launcher """
    click.echo(click.style("Initializing scenario ⏱", fg="magenta"))

    with RuntimeDevice(configurator) as rt:
        pass


def configure_scenario():
    """
    """
    pass
