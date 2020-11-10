"""
    This module contains a configurator object for SymuVia. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation. The objective is to introduce flexibility when configuring the the simulator platform and the runtime execution possibilities offered by exposed functions from the c library of SymuVia
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click
import platform
from dataclasses import dataclass

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.connector_configurator import ConnectorConfigurator
from symupy.utils.configurator import Configurator as SymupyConfigurator
import ensemble.tools.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class SymuviaConfigurator(ConnectorConfigurator, SymupyConfigurator):
    """Configurator class for containing specific simulator parameters for
        Symuvia

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

        :return: Configurator object with simulation parameters
        :rtype: Configurator
    """

    library_path: str = CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]

    def __init__(self, **kwargs) -> None:
        """ Configurator class for containing specific simulator parameter

            Args:

            buffer_string (int):
                Size of the buffer for message for data received from simulator

            write_xml (bool):
                Flag to turn on writting the XML output

            trace_flow (bool):
                Flag to determine tracing or not the flow / trajectories

            library_path (str):
                Absolute path towards the simulator library

            total_steps (int):
                Define the number of iterations of a simulation

            step_launch_mode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``
        """
        ConnectorConfigurator()
        SymupyConfigurator.__init__(self, **kwargs)
