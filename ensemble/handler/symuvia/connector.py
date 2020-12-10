"""
Symuvia Connector
=================
This module details the implementation of a ``Simulator`` object in charge of handling the connection between the traffic simulator and this interface. The connection with the traffic simulator is handled by an object called ``Connector`` which establishes a messaging protocol with the traffic simulator. 

Example:
    To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

        >>> from ensemble.handler.symuvia import SymuviaConnector
        >>> path_symuvia = "path/to/libSymuyVia.dylib"
        >>> simulator = SymuviaConnector(library_path=path_symuvia)

Other parameters can also be send to the simulator in order to provide other configurations:

Example: 
    To send make increase the *buffer size* to a specific size:

        >>> simulator = Simulator(path, bufferSize = 1000000)
    
    To increase change the flag that traces the flow:

        >>> simulator = Simulator(path, traceFlow = True)
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click
from pathlib import Path

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .stream import SimulatorRequest
from .configurator import SymuviaConfigurator
from .scenario import SymuviaScenario

from ensemble.metaclass.connector import AbsConnector

from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)

from ensemble.tools.screen import log_verify, log_success, log_error

import ensemble.tools.constants as CT


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymuviaConnector(SymuviaConfigurator, AbsConnector):
    """ 
        Simulator class for containing object to connect and  command a simulation in SymuVia

        Example:
            Call of the default simulator ::

                >>> from symupy.api import Simulator
                >>> simulator = Simulator()

        :return: Symuvia simulator object with simulation parameters
        :rtype: Simulator

        You may also pass suplementary parameters to the object by specifying keys in the call: 

        Example: 
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> from symupy.api import Simulator
                >>> path_symuvia = "path/to/libSymuyVia.dylib"
                >>> simulator = Simulator(library_path=path_symuvia)
    
        This object describes is a configurator manager for the interface between the traffic simulator and the python interface. For more details on the optinal keyword parameters please refer to :py:class:`~symupy.utils.configurator.Configurator` class.

        :raises SymupyLoadLibraryError: 
            Error raised whenever the SymuVia library is not found

        :raises SymupyFileLoadError: 
            Error raised whenever the provided path for an scenario cannot be loaded into the Simulator

        :raises SymupyVehicleCreationError: 
            Error raised when a vehicle cannot be created

        :raises SymupyDriveVehicleError: 
            Error rased when a vehicle state cannot be imposed

        :raises NotImplementedError: 
            Not implemented functionality 

        :return: Simulator manager object 

        :rtype: Simulator
    """

    def __init__(self, **kwargs,) -> None:
        SymuviaConfigurator.__init__(self, **kwargs)
        AbsConnector.__init__(self)
        self.load_simulator()

    # ========================================================================
    # LOADING METHODS
    # ========================================================================

    def load_simulator(self) -> None:
        """ 
            This is a method to load the shared symuvia library into python. This method
            is used in the internal simulationp process however it can be also called from 
            outside like:

            Example:
                To use the ``Simulator`` declare in a string the ``path`` to the simulator ::
                    
                    >>> from ensemble.tools.constants import DEFAULT_LIB_OSX
                    >>> simulator = Simulator(DEFAULT_LIB_OSX) 
                    >>> simulator.load_symuvia()

            Raises:
                EnsembleAPILoadLibraryError: When the library cannot be loaded
        """
        try:
            lib_symuvia = cdll.LoadLibrary(self.library_path)
            log_success("\t Library successfully loaded!")
        except OSError:
            log_error("\t SymuVia is currently unavailable!")
            raise EnsembleAPILoadLibraryError(
                "Library not found", self.library_path
            )
        self.__library = lib_symuvia

    def load_scenario(self, scenario: SymuviaScenario):
        """ checks existance and load scenario into 
        """
        if isinstance(scenario, SymuviaScenario):
            try:
                self.__library.SymLoadNetworkEx(scenario.filename("UTF8"))
                self.performInitialize(scenario)
                self.simulation = scenario
                log_verify("\t Scenario successfully loaded!")
                return
            except:
                raise EnsembleAPILoadFileError(
                    f"\t Simulation could not be loaded"
                )
        EnsembleAPIWarning(f"\tSimulation could not be loaded.")

    def register_simulation(self, scenarioPath: str) -> None:
        """
            Register simulation file within the simulator

            :param scenarioPath: Path to scenario 
            :type scenarioPath: str
        """
        self.simulation = SymuviaScenario(scenarioPath)

    def request_answer(self):
        """
            Request simulator answer and maps the data locally
        """
        if self.step_launch_mode == "lite":
            self._bContinue = self.__library.SymRunNextStepLiteEx(
                self.write_xml, byref(self.b_end)
            )
            return
        self._bContinue = self.__library.SymRunNextStepEx(
            self.buffer_string, self.write_xml, byref(self.b_end)
        )
        self.request.query = self.buffer_string

    def query_data(self) -> int:
        """ Run simulation step by step

        :return: iteration step
        :rtype: int
        """
        try:
            self.request_answer()
            self._c_iter = next(self._n_iter)
            return self._c_iter
        except StopIteration:
            self._bContinue = False
            return -1

    # ==========================================================================
    # PROTOCOLS
    # ==========================================================================

    def performConnect(self) -> None:
        """
             Perform simulation connection
        """
        self.load_simulator()

    def performInitialize(self, scenario: SymuviaScenario) -> None:
        """
            Perform simulation initialization
        """
        self.request = SimulatorRequest()
        self._n_iter = iter(scenario.get_simulation_steps())
        self._c_iter = next(self._n_iter)
        self._bContinue = True

    def performPreRoutine(self) -> None:
        """
            Perform simulator preroutine
        """
        raise NotImplementedError

    def performQuery(self) -> None:
        """
            Perform simulator Query
        """
        raise NotImplementedError

    # ==========================================================================
    # ATTRIBUTES
    # ==========================================================================

    @property
    def scenariofilename(self):
        """ Scenario filenamme
        
            Returns: 
                filname (str): Absolute path towards the XML input for SymuVia

        """
        return self.simulation.filename()

    @property
    def get_vehicle_data(self):
        """Returns the query received from the simulator

            :return: Request from the simulator
            :rtype: dict
        """
        return self.request.get_vehicle_data()

    @property
    def simulation_step(self):
        """ Current simulation iteration"""
        return self._c_iter
