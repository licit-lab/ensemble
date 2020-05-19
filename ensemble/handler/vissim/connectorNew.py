# ============================================================================
# INTERNAL IMPORTS
# ============================================================================
import click
from .stream import SimulatorRequest
from .configurator import VissimConfigurator
from .scenario import VissimScenario

from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)
try:
    import win32com.client as com
    from pywintypes import com_error
except ModuleNotFoundError:
    click.echo(click.style("\t Platform non compatible with Windows", fg="yellow"))
import ensemble.tools.constants as CT


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class VissimConnector(VissimConfigurator):
    # def __init__(self):
    #     super(VissimConnector, self).__init__()

    def __init__(self, path: str) -> None:
        self._path = path  # "Vissim.Vissim-64.10"# path
        self.load_vissim()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryname})"

    def load_vissim(self) -> None:
        """ load Vissim COM interface"""
        try:
            lib_vissim = com.gencache.EnsureDispatch(self._path)
            click.echo(click.style(f"\t Library successfully loaded!", fg="green", bold=True))
        except OSError:
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        except com_error:
            click.echo(click.style(f"\t Visssim is currently unavailable!", fg="red", bold=True))
            lib_vissim = None
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        self._library = lib_vissim

    def load_scenario(self, scenario: VissimScenario):
        """ checks existance and load scenario into
        """
        if isinstance(scenario, VissimScenario):
            try:
                self._library.LoadNet(scenario.filename, scenario.bread_additional)
                #self.sim_period = self._library.Simulation.AttValue('SimPeriod')
                #self.sim_sec = self._library.Simulation.AttValue('SimSec')
                #self.sim_res = self._library.Simulation.AttValue('SimRes')
                #self.rand_seed = self._library.Simulation.AttValue('RandSeed')
                #self.performInitialize(scenario)
                #self.simulation = scenario
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
        self.simulation = VissimScenario(scenarioPath)

    def request_answer(self):
        """
            Request simulator answer and maps the data locally
        """
        vehsAttributesNamesVissim = ('CoordFrontX', 'Acceleration', 'Pos', 'No', 'CoordFrontY', 'Lane\\Link\\No', 'VehType', 'Speed', 'Lane\\Index')
        vehsAttributes = self._library.Net.Vehicles.GetMultipleAttributes(vehsAttributesNamesVissim)
        self.request.parse_data(vehsAttributes)
    def run_single_step(self):
        self._library.Simulation.RunSingleStep()

    def query_data(self) -> int:
        """ Run simulation step by step

        :return: iteration step
        :rtype: int
        """
        try:
            self.request_answer()
            self.run_single_step()
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
        self.load_vissim()

    def performInitialize(self, scenario: VissimScenario) -> None:
        """
            Perform simulation initialization
        """
        #self._b_end = c_int()
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


    def get_simulation_steps(self) -> range:
        return range(0,self.sim_period,self.sim_res)
    def get_vehicletype_information(self) -> tuple:
        """ Get the vehicle parameters

        :return: tuple of dictionaries containing vehicle parameters
        :rtype: tuple
        """
        vehTypesAttributes = self._library.Net.VehicleTypes.GetMultipleAttributes(['No', 'Name'])
        return vehTypesAttributes
    def get_network_links(self) -> tuple:
        """ Get network link names

        :return: tuple containing link names
        :rtype: tuple
        """
        # GetMultiAttValues         Read one attribute of all objects:
        Attribute = "Name"
        NameOfLinks= self._library.Net.Links.GetMultiAttValues(Attribute)
        # NameOfLinks = toList(NameOfLinks)  # convert to list
        return NameOfLinks




