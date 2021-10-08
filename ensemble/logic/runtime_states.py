""" 
Runtime States
==============
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

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.state import AbsState
from ensemble.tools.checkers import check_scenario_consistency
from ensemble.tools.exceptions import (
    EnsembleAPILoadLibraryError,
    EnsembleAPILoadFileError,
)
from ensemble.tools.screen import (
    log_in_terminal,
    log_warning,
    log_error,
    log_verify,
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Compliance(AbsState):
    """
    The state which declares an status to check file compliance .
    """

    def next_state(self, event: str, configurator) -> AbsState:
        """Returns next state

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
            log_error("Something happened with the files")
            return Terminate()

    def perform_check(self, configurator):
        """This function triggers the check validation for the files raises errors in case files are not found

        :param configurator: Configuration descriptor
        :type configurator: Configurator
        """
        return check_scenario_consistency(configurator)


class Connect(AbsState):
    """
    The state which declares the creation of a connection with the simulator
    """

    def next_state(self, event: str, configurator) -> AbsState:

        try:
            configurator.load_socket()
        except EnsembleAPILoadLibraryError:
            log_warning("\tLibrary could not be loaded.\n\tEnding simulation")
            return Terminate()

        if event == "initialize":
            return Initialize()

        return self


class Initialize(AbsState):
    """
    The state which initializes values for the scenario simulation
    """

    def next_state(self, event: str, configurator) -> AbsState:

        try:
            configurator.load_scenario()
        except EnsembleAPILoadFileError:
            log_warning("\tScenario could not be loaded.\n\tEnding simulation")
            return Terminate()

        if event == "preroutine":
            log_in_terminal("Start of Runtime ⏱", fg="magenta")
            return PreRoutine()

        return self


class PreRoutine(AbsState):
    """
    The state which performs task previous to the interaction with the simulator
    """

    def next_state(self, event: str, configurator) -> AbsState:
        if event == "query":
            return Query()

        return self


class Query(AbsState):
    """
    The state which retrieves information from the simulator
    """

    def next_state(self, event: str, configurator) -> AbsState:

        # TODO: call simulator step by step.

        if event == "control":

            # Retrieves data
            configurator.query_data()  # Retreives data + update_registry

            # Updates platoon registry
            configurator.update_platoon_registry()

            if configurator.verbose:
                log_verify("Vehicle registry:")
                log_in_terminal(
                    configurator.vehicle_registry.pretty_print(
                        ["abscissa", "ordinate", "acceleration", "speed"]
                    ),
                )
                log_verify("Platoon Registry:")
                log_in_terminal(
                    configurator.platoon_registry.pretty_print(
                        [
                            "state",
                            "platoon",
                            "comv2x",
                            "abscissa",
                            "ordinate",
                            "acceleration",
                            "speed",
                            "distance",
                            "driven",
                        ]
                    ),
                )
            return Control()

        return self


class Control(AbsState):
    """
    The state which computes the control decision
    """

    def next_state(self, event: str, configurator) -> AbsState:
        if event == "push":
            # configurator.platoon_registry.apply_cacc(
            #     configurator.connector.time
            # )
            return Push()
        return self


class Push(AbsState):
    """
    The state which pushes data back to the simulator
    """

    def next_state(self, event: str, configurator) -> AbsState:
        if event == "postroutine":
            return PostRoutine()
        # TODO: Add methods
        # configurator.push_data()
        return self


class PostRoutine(AbsState):
    """
    The state which logs information or compute step indicators
    """

    def next_state(self, event: str, configurator) -> AbsState:
        if event == "preroutine" and configurator.connector.do_next:
            return PreRoutine()
        elif event == "terminate":
            return Terminate()
        elif not configurator.connector.do_next:
            return Terminate()

        return self


class Terminate(AbsState):
    """
    The state which declares the end of a simulation
    """

    def next_state(self, event: str, configurator) -> AbsState:
        log_in_terminal("End of Runtime ⏱", fg="magenta")
        return self


# End of our states.
