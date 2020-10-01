"""
    This module contains a base configurator to support methods and properties for the connector particularly tied to the ENSEMBLE project. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class ConnectorConfigurator:
    """ Base Configurator class for containing specific simulator parameters

        :return: Configurator object with methods for printing
        :rtype: Configurator
    """

    def __repr__(self):
        data_dct = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = "Configuration status:\n " + "\n ".join(f"{k}:  {v}" for k, v in self.__dict__.items())
        return f"{data_dct}"
