"""
    This module contains a configurator object for SymuVia. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation. The objective is to introduce flexibility when configuring the the simulator platform and the runtime execution possibilities offered by exposed functions from the c library of SymuVia
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import create_string_buffer, c_bool, c_char, c_int
from dataclasses import dataclass
import click
import platform

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.constants import (
    BUFFER_STRING,
    WRITE_XML,
    TRACE_FLOW,
    TOTAL_SIMULATION_STEPS,
    LAUNCH_MODE,
)

from symupy.utils.constants import DEFAULT_PATH_SYMUVIA

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

from ensemble.tools.connector_configurator import ConnectorConfigurator
from ensemble.tools.screen import log_verify
import ensemble.tools.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class SymuviaConfigurator(ConnectorConfigurator):
    """ Configurator class for containing specific simulator parameters
        Example:
            To use the ``Simulator`` declare in a string the ``path`` to the
            simulator ::

                >>> path = "path/to/libSymuyVia.dylib"
                >>> simulator = SymuviaConfigurator(library_path = path)

        Args:
            library_path (str):
                Absolute path towards the simulator library

            bufferSize (int):
                Size of the buffer for message for data received from simulator

            write_xml (bool):
                Flag to turn on writting the XML output

            trace_flow (bool):
                Flag to determine tracing or not the flow / trajectories

            total_steps (int):
                Define the number of iterations of a simulation

            step_launch_mode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``

        Returns: 
            configurator (Configurator): 
                Configurator object with simulation parameters
    """

    buffer_string: c_char = create_string_buffer(BUFFER_STRING)
    write_xml: c_bool = c_bool(WRITE_XML)
    trace_flow: bool = TRACE_FLOW
    library_path: str = DEFAULT_PATH_SYMUVIA
    total_steps: int = TOTAL_SIMULATION_STEPS
    step_launch_mode: str = LAUNCH_MODE
    library_path: str = CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]
    b_end: c_int = c_int()

    def __init__(self, **kwargs) -> None:
        """ Configurator class for containing specific simulator parameter

            Args:
                library_path (str):
                    Absolute path towards the simulator library

                bufferSize (int):
                    Size of the buffer for message for data received from simulator

                write_xml (bool):
                    Flag to turn on writting the XML output

                trace_flow (bool):
                    Flag to determine tracing or not the flow / trajectories

                total_steps (int):
                    Define the number of iterations of a simulation

                step_launch_mode (str):
                    Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``
        """
        log_verify(f"{self.__class__.__name__}: Initialization")
        for key, value in kwargs.items():
            setattr(self, key, value)
