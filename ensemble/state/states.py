""" 
    This module defines the basic states required to execute and launch a simulation. 

    The states are defined as: 

    * **Compliance**: This state is defined to check availability of files and candidates.
    * **Connect**: This state is defined to process 
    * **Initialize**: This state perform initialization tasks. In example, loading the file scenarios into the simulator. Declaring initial conditions for the platoon, etc. 
    * **Preroutine**: Tasks to be done before the querying information from the simulator
    * **Query**: Tasks of parsing data and querying information from the simulator
    * **Control**: Perform decision tasks for the platoon 
    * **Push**: Push updated information to the simulator for platoon vehicles 
    * **Postroutine**: Performs tasks after the information has been pushed. 
"""

from .base import State
import click

from ensemble.tools.checkers import check_scenario_consistency
from ensemble.tools.exceptions import EnsembleAPILoadLibraryError

# Start of our states
class Compliance(State):
    """
    The state which declares an status to check file compliance .
    """

    def on_event(self, event: str, configurator) -> None:
        """ Returns next state 
        
        :param event: Event keyword for next state "connect"
        :type event: str
        :return: Connect object in case of switch
        :rtype: Connect
        """
        try:
            # REVIEW: This logic is too simplistic. Double check conditions for continuing
            if event == "connect" and self.perform_check(configurator):
                return Connect()
            return self
        except:
            click.echo("Something happened with the files")
            return Terminate()

    def perform_check(self, configurator):
        """ This function triggers the check validation for the files raises errors in case files are not found 
        
        :param configurator: Configuration descriptor 
        :type configurator: Configurator
        """
        return check_scenario_consistency(configurator)


class Connect(State):
    """
    The state which declares the creation of a connection with the simulator
    """

    def on_event(self, event: str, configurator):

        try:
            configurator.load_socket()
        except EnsembleAPILoadLibraryError:
            click.echo(click.style(f"\tLibrary could not be loaded.\n\tEnding simulation", fg="yellow",))
            return Terminate()

        if event == "initialize":
            return Initialize()

        return self


class Initialize(State):
    """
    The state which initializes values for the scenario simulation
    """

    def on_event(self, event: str, configurator):
        if event == "preroutine":
            return PreRoutine()

        return self


class PreRoutine(State):
    """
    The state which performs task previous to the interaction with the simulator
    """

    def on_event(self, event: str, configurator):
        if event == "query":
            return Query()

        return self


class Query(State):
    """
    The state which retrieves information from the simulator
    """

    def on_event(self, event: str, configurator):
        if event == "control":
            return Control()

        return self


class Control(State):
    """
    The state which computes the control decision  
    """

    def on_event(self, event: str, configurator):
        if event == "push":
            return Push()

        return self


class Push(State):
    """
    The state which pushes data back to the simulator
    """

    def on_event(self, event: str, configurator):
        if event == "postroutine":
            return PostRoutine()

        return self


class PostRoutine(State):
    """
    The state which logs information or compute step indicators 
    """

    def on_event(self, event: str, configurator):
        if event == "preroutine":
            return PreRoutine()
        elif event == "terminate":
            return Terminate()

        return self


class Terminate(State):
    """
    The state which declares the end of a simulation
    """

    def on_event(self, event: str, configurator):
        click.echo(click.style("Succesfully accomplished ⏱", fg="magenta"))
        return self


# End of our states.
