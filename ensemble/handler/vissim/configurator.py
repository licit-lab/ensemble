"""
    This module contains a ``Configurator`` object for Vissim. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation.
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform
from dataclasses import dataclass

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.connector_configurator import ConnectorConfigurator
from ensemble.tools.screen import log_verify
import ensemble.tools.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class VissimConfigurator(ConnectorConfigurator):
    """ Configurator class for containing specific simulator parameters for     
        Vissim

        Example:
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> path = "path/to/simluator.so"
                >>> simulator = VissimConfigurator(library_path = path)

        Args:
            library_path (str):
                Absolute path towards the simulator library

        :return: Configurator object with simulation parameters
        :rtype: Configurator
    """

    library_path: str = CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]

    def __init__(self, **kwargs) -> None:
        """ Configurator class for containing specific simulator parameter
            :param libraryPath: Stores the path of a traffic simulator, defaults to ""
            :type libraryPath: str, optional
            :param totalSteps: total number of simulation steps, defaults to 0
            :type totalSteps: int, optional
            :return: Configurator object with simulation parameters
            :rtype: Configurator
        """
        log_verify(f"{self.__class__.__name__}: Initialization")
        ConnectorConfigurator()
        self.libraryPath = kwargs.get("libraryPath", "")
        self.totalSteps = kwargs.get("totalSteps", 0)
