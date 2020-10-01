"""
    This module contains a configurator object for SymuVia. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation. The objective is to introduce flexibility when configuring the the simulator platform and the runtime execution possibilities offered by exposed functions from the c library of SymuVia
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click
import platform

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.connector_configurator import ConnectorConfigurator
from symupy.utils.configurator import Configurator as SymupyConfigurator
import ensemble.tools.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymuviaConfigurator(ConnectorConfigurator, SymupyConfigurator):
    """ Configurator class for containing specific simulator parameters for SymuVia

        Example:
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> path = "path/to/simluator.so"
                >>> simulator = SymuviaConfigurator(libraryPath = path)

        :return: Symuvia Configurator object with simulation parameters
        :rtype: SymuviaConfigurator
    """

    def __init__(
        self,
        bufferSize: int = CT.BUFFER_STRING,
        writeXML: bool = CT.WRITE_XML,
        traceFlow: bool = CT.TRACE_FLOW,
        libraryPath: str = CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())],
        totalSteps: int = CT.TOTAL_SIMULATION_STEPS,
        stepLaunchMode: str = CT.LAUNCH_MODE,
    ) -> None:
        """  Symuvia Configurator class for containing specific simulator parameter

            :param bufferSize: Provide an integer for buffer, defaults to CT.BUFFER_STRING
            :type bufferSize: int, optional
            :param writeXML: Flag to write XML file, defaults to True
            :type writeXML: bool, optional
            :param traceFlow: Flag to trace Flow / Traces, defaults to False
            :type traceFlow: bool, optional
            :param libraryPath: Stores the path of a traffic simulator, defaults to ""
            :type libraryPath: str, optional
            :param totalSteps: total number of simulation steps, defaults to 0
            :type totalSteps: int, optional
            :param stepLaunchMode: lite / full, defaults to "lite"
            :type stepLaunchMode: str, optional
            :return: Configurator object with simulation parameters
            :rtype: Configurator
        """
        super(SymuviaConfigurator, self).__init__(
            bufferSize=bufferSize,
            writeXML=writeXML,
            traceFlow=traceFlow,
            libraryPath=libraryPath,
            totalSteps=totalSteps,
            stepLaunchMode=stepLaunchMode,
        )
