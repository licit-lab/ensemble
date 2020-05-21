"""
    This module contains a ``Configurator`` object. The configurator is an object that stores *parameters* that can be relevant to make the evolution of a simulation.
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import ensemble.tools.constants as CT


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class VissimConfigurator:
    """ Configurator class for containing specific simulator parameters

        Example:
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> path = "path/to/simluator.so"
                >>> simulator = Configurator(libraryPath = path)


        :return: Configurator object with simulation parameters
        :rtype: Configurator
    """

    def __init__(self,
            libraryPath: str = "",
            totalSteps: int = 0) -> None:
        """ Configurator class for containing specific simulator parameter
            :param libraryPath: Stores the path of a traffic simulator, defaults to ""
            :type libraryPath: str, optional
            :param totalSteps: total number of simulation steps, defaults to 0
            :type totalSteps: int, optional
            :return: Configurator object with simulation parameters
            :rtype: Configurator
        """
        click.echo("Configurator: Initialization")
        self.libraryPath = libraryPath
        self.totalSteps = totalSteps
        super(VissimConfigurator, self).__init__()

    def __repr__(self):
        data_dct = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = "Configuration status:\n " + "\n ".join(f"{k}:  {v}" for k, v in self.__dict__.items())
        return f"{data_dct}"
