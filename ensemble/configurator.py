""" 
Configurator
====================================
A class to store parameters for runtime execution
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import click
from dataclasses import dataclass, field
import platform
from typing import List, Any, Dict

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


from ensemble.tools.constants import (
    DCT_DEFAULT_PATHS,
    DCT_SIMULATORS,
    DCT_RUNTIME_PARAM,
)
from ensemble.handler.symuvia import SymuviaConnector, SymuviaScenario
from ensemble.handler.vissim.connector import VissimConnector, VissimScenario

# from ensemble.control.governor import MultiBrandPlatoonRegistry
from ensemble.component.vehiclelist import VehicleList
from ensemble.control.tactical.gapcordinator import GlobalGapCoordinator
from ensemble.tools.screen import log_success, log_verify, log_warning

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class Configurator:
    """Configurator class for containing specific simulator parameter

    Args:

    verbose (bool):
        Indicates if verbosity is required within the exit

    info (bool):
        Prints project information

    platform (str):
        Platform to run: Windows, Darwin, Linux

    simulation_platform (str):
        Traffic simulation platform: vissim, symuvia

    scenario_files (list):
        List of absolute files containing traffic scenarios

    simulation_parameters (dict):
        List of simulatio parameters. Check ``constants`` module for more information
    """

    verbose: bool = False
    info: bool = True
    platform: str = platform.system()
    simulation_platform: str = ""
    library_path: str = ""

    def __init__(self, **kwargs) -> None:
        """Configurator class for containing specific simulator parameter

        Args:

        verbose (bool):
            Indicates if verbosity is required within the exit

        info (bool):
            Prints project information

        platform (str):
            Platform to run: Windows, Darwin, Linux

        simulation_platform (str):
            Traffic simulation platform: vissim, symuvia

        scenario_files (list):
            List of absolute files containing traffic scenarios

        simulation_parameters (dict):
            List of simulatio parameters. Check ``constants`` module for more information
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.scenario_files = []
        self.simulation_parameters = DCT_RUNTIME_PARAM

    def set_simulation_platform(self, simulation_platform: str = "") -> None:
        """A simpler setter for the simulation platform based on OS

        Args:
            simulation_platform (str): "symuvia" or "vissim", defaults to ""
        """
        if simulation_platform:
            self.simulation_platform = simulation_platform
            return

        log_verify("Solving platform ", bold=True)

        self.simulation_platform = DCT_SIMULATORS.get(self.platform, "")

        if self.verbose:
            log_warning(
                "Setting default simulation platform platform",
                "\t{(self.simulation_platform, self.platform)}",
            )

        key = (self.simulation_platform, self.platform)
        self.library_path = DCT_DEFAULT_PATHS[key]

        log_success(
            "Simulator path set to default value:", f"\t{self.library_path}"
        )
        return

    def update_values(self, **kwargs) -> None:
        """Configurator updater, pass a with keyword arguments to update.
        Just pass the desired parameter as a kewyword argument.
        """

        if kwargs.get("library_path"):

            self.library_path = kwargs.get("library_path", self.library_path)

            log_verify(
                "Setting new library path to user input:",
                f"\t{self.library_path}",
            )

        if kwargs.get("scenario_files"):
            self.scenario_files = kwargs.get(
                "scenario_files", self.scenario_files
            )

            log_verify(
                "Setting new scenario file(s) path to user input:",
                f"\t{self.scenario_files}",
            )

    def load_socket(self):
        """ Determines simulation platform to connect """
        if self.simulation_platform == "symuvia":
            self.connector = SymuviaConnector(
                library_path=self.library_path, step_launch_mode="traj"
            )
        else:
            self.connector = VissimConnector(library_path=self.library_path)

    def load_scenario(self):
        self.scenario_files = tuple(self.scenario_files)
        if self.simulation_platform == "symuvia":
            scenario = SymuviaScenario.create_input(
                *self.scenario_files
            )  # expected input (fileA,fileB)
        else:
            scenario = VissimScenario.create_input(
                *self.scenario_files
            )  # expected input (fileA,fileB)

        # Call connector (automatic dispatch)
        self.connector.load_scenario(scenario)

    def query_data(self):
        self.connector.query_data()

    def create_vehicle_registry(self):
        """ Creates a vehicle registry for all vehicles in simulation """
        self.vehicle_registry = VehicleList(self.connector.request)

    def update_vehicle_registry(self):
        """ Updates vehicle registry in case it exists"""
        if hasattr(self, "vehicle_registry"):
            self.vehicle_registry.update_list()
            return
        self.create_vehicle_registry()

    def create_platoon_registry(self):
        """ Creates a platoon registry for all coordinators (FGC-RGC) """
        self.platoon_registry = GlobalGapCoordinator(self.vehicle_registry)

    def update_platoon_registry(self):
        if hasattr(self, "platoon_registry"):
            self.platoon_registry.update_platoons()
            return
        self.create_platoon_registry()

    @property
    def total_steps(self):
        return self.simulation_parameters.get("total_steps")


if __name__ == "__main__":
    Configurator()
