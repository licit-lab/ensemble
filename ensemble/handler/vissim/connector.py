"""
    This module contains objects for modeling a simplified connector to handle vissim
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from .stream import SimulatorRequest
from .configurator import VissimConfigurator
from .scenario import VissimScenario

from ensemble.metaclass.connector import AbsConnector


from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)

from ensemble.tools.screen import (
    log_verify,
    log_success,
    log_error,
    log_warning,
)

import ensemble.tools.constants as CT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

try:
    import win32com.client as com
    from pywintypes import com_error
except ModuleNotFoundError:
    log_warning("\t Platform non compatible with Windows")


class VissimConnector(AbsConnector, VissimConfigurator):
    """
    This models a connector and interactions from the API with the Vissim library.

    :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

    def __init__(self, **kwargs) -> None:
        AbsConnector.__init__(self)
        VissimConfigurator.__init__(self, **kwargs)
        self.load_simulator()

    def load_simulator(self) -> None:
        """load Vissim COM interface"""
        try:
            lib_vissim = com.gencache.EnsureDispatch(self.library_path)
            log_success("\t Library successfully loaded!")
        except OSError:
            log_error("\t Vissim is currently unavailable!")
            raise EnsembleAPILoadLibraryError(
                "Library not found", self.library_path
            )
        except com_error:
            log_error("\t Vissim is currently unavailable!")
            lib_vissim = None
            raise EnsembleAPILoadLibraryError(
                "Library not found", self.library_path
            )
        self.__library = lib_vissim

    def load_scenario(self, scenario):
        """checks existance and load scenario . Also get simulation parameters"""
        if isinstance(scenario, VissimScenario):
            try:
                self.__library.LoadNet(
                    scenario.filename, scenario.bread_additional
                )
                self.sim_period = self.__library.Simulation.AttValue(
                    "SimPeriod"
                )
                self.sim_sec = self.__library.Simulation.AttValue("SimSec")
                self.sim_res = self.__library.Simulation.AttValue("SimRes")
                self.rand_seed = self.__library.Simulation.AttValue("RandSeed")
                self.performInitialize(scenario)
                self.simulation = scenario
                log_verify("\t Scenario successfully loaded!")
                return
            except:
                raise EnsembleAPILoadFileError(
                    f"\t Simulation network could not be loaded"
                )
            try:
                self.__library.LoadLayout(scenario.filename_layx)
                return
            except:
                raise EnsembleAPILoadFileError(
                    f"\t Simulation layout could not be loaded"
                )
        EnsembleAPIWarning(f"\tSimulation could not be loaded.")

    def register_simulation(self, scenarioPath: str) -> None:
        """
        Register simulation file within the simulator

        :param scenarioPath: Path to scenario
        :type scenarioPath: str
        """
        self.simulation = VissimScenario(scenarioPath)

    def request_answer(self):
        """
        Request simulator answer and maps the data locally
        """
        vehsAttributesNamesVissim = (
            "CoordFrontX",
            "Acceleration",
            "Pos",
            "No",
            "CoordFrontY",
            "Lane\\Link\\No",
            "VehType",
            "Speed",
            "Lane\\Index",
        )
        vehsAttributes = self.__library.Net.Vehicles.GetMultipleAttributes(
            vehsAttributesNamesVissim
        )
        vehData = [
            dict(zip(vehsAttributesNamesVissim, item))
            for item in vehsAttributes
        ]
        self.request.query = vehData  # List[Dicts]
        self.request.sim_sec = self.__library.Simulation.AttValue(
            "SimSec"
        )  # self.sim_sec

    def run_single_step(self):
        """Run simulation next step

        :return: None
        :rtype: None
        """
        self.__library.Simulation.RunSingleStep()

    def query_data(self) -> int:
        """Run simulation step by step

        :return: iteration step
        :rtype: int
          To test query, you can use click.echo(self.get_vehicle_data()) after request_answer()
        """
        try:
            self.request_answer()
            self.run_single_step()
            self._c_iter = next(self._n_iter)
            return self._c_iter
        except StopIteration:
            self._bContinue = False
            return -1

    def push_data(self):
        """Pushes data back to the simulator"""
        pass

    # =========================================================================
    # PROTOCOLS
    # =========================================================================

    def performConnect(self) -> None:
        """
        Perform simulation connection
        """
        self.load_simulator()

    def performInitialize(self, scenario: VissimScenario) -> None:
        """
        Perform simulation initialization
        """
        self.request = SimulatorRequest()
        self._n_iter = iter(self.get_simulation_steps())
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

    # =========================================================================
    # ATTRIBUTES
    # =========================================================================

    def get_simulation_steps(self) -> range:
        """Gets the list of simulation steps starting from 0 to end of simulation in step of simulation resolution"""
        return range(0, self.sim_period, self.sim_res)

    @property
    def scenariofilename(self):
        """Scenario filenamme

        Returns:
            filname (str): Absolute path towards the XML input for SymuVia

        """
        return self.simulation.filename

    @property
    def get_vehicle_data(self):
        """Returns the query received from the simulator

        :return: Request from the simulator
        :rtype: dict
        """
        return self.request.get_vehicle_data()

    @property
    def simulation_step(self):
        """Current simulation iteration"""
        return self._c_iter
