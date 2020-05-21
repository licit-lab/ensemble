"""
    **SymuVia Connector Module**

    This module details the implementation of a ``Simulator`` object in charge of handling the connection between the traffic simulator and this interface. The connection with the traffic simulator is handled by an object called ``Connector`` which establishes a messaging protocol with the traffic simulator. 

    Example:
        To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

            >>> path = "path/to/simulator.so"
            >>> simulator = Simulator(path) 

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

from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)
import ensemble.tools.constants as CT


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymuviaConnector(SymuviaConfigurator):
    """ 
        This models a connector and interactions from the API with the Symuvia library. 

        :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

    def __init__(
        self,
        libraryPath: str = "",
        bufferSize: int = CT.BUFFER_STRING,
        writeXML: bool = True,
        traceFlow: bool = False,
        totalSteps: int = 0,
        stepLaunchMode: str = "lite",
        **kwargs,
    ) -> None:
        super(SymuviaConnector, self).__init__(
            bufferSize=bufferSize,
            writeXML=writeXML,
            traceFlow=traceFlow,
            libraryPath=libraryPath,
            totalSteps=totalSteps,
            stepLaunchMode=stepLaunchMode,
            **kwargs,
        )
        self.load_symuvia()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryPath})"

    # ============================================================================
    # LOADING METHODS
    # ============================================================================

    def load_symuvia(self) -> None:
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
            lib_symuvia = cdll.LoadLibrary(self.libraryPath)
            click.echo(click.style(f"\t Library successfully loaded!", fg="green", bold=True))
        except OSError:
            click.echo(click.style(f"\t SymuVia is currently unavailable!", fg="red", bold=True,))
            raise EnsembleAPILoadLibraryError("Library not found", self.libraryPath)
        self.__library = lib_symuvia

    def load_scenario(self, scenario: SymuviaScenario):
        """ checks existance and load scenario into 
        """
        if isinstance(scenario, SymuviaScenario):
            try:
                self.__library.SymLoadNetworkEx(scenario.filename("UTF8"))
                self.performInitialize(scenario)
                self.simulation = scenario
                return
            except:
                raise EnsembleAPILoadFileError(f"\t Simulation could not be loaded")
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
        if self.stepLaunchMode == "lite":
            self._bContinue = self.__library.SymRunNextStepLiteEx(self.writeXML, byref(self._b_end))
            return
        self._bContinue = self.__library.SymRunNextStepEx(self.bufferString, self.writeXML, byref(self._b_end))
        self.request.query = self.bufferString

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

    # ============================================================================
    # PROTOCOLS
    # ============================================================================

    def performConnect(self) -> None:
        """
             Perform simulation connection
        """
        self.load_symuvia()

    def performInitialize(self, scenario: SymuviaScenario) -> None:
        """
            Perform simulation initialization
        """
        self._b_end = c_int()
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

    # ============================================================================
    # ATTRIBUTES
    # ============================================================================

    def scenarioFilename(self, encoding=None) -> str:
        """ 
            Scenario filenamme
        
            :return: Absolute path towards the XML input for SymuVia
            :rtype: str
        """
        return self.simulation.filename(encoding)

    # @property
    # def s_response_dec(self):
    #     """
    #         Obtains instantaneous data from simulator

    #         :return: last query from simulator
    #         :rtype: str
    #     """
    #     return self.bufferString.value.decode("UTF8")

    # @property
    # def do_next(self) -> bool:
    #     """
    #         Returns true if the simulation shold continue

    #         :return: True if next step continues
    #         :rtype: bool
    #     """
    #     return self._bContinue

    @property
    def get_vehicle_data(self) -> dict:
        """
            Returns the query received from the simulator

            :return: Request from the simulator
            :rtype: dict
        """
        return self.request.vehicles

    # @property
    # def simulation(self) -> Simulation:
    #     """
    #         Simulation scenario

    #         :return: Object describing senario under simulation
    #         :rtype: Simulation
    #     """
    #     return self._sim

    # @property
    # def simulationstep(self) -> str:
    #     """
    #         Current simulation step.

    #         Example:
    #             You can use the time step to control actions

    #             >>> with simulator as s:
    #             ...     while s.do_next()
    #             ...         if s.simulationstep>0:
    #             ...             print(s.simulationtimestep)

    #         :return: current simulation iteration
    #         :rtype: str
    #     """
    #     return self._c_iter
