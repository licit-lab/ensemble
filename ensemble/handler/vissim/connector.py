"""
    This module contains objects for modeling a simplified connector to handle vissim
"""

import click
from .stream import SimulatorRequest
from .configurator import VissimConfigurator
from .scenario import VissimScenario

from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)
import ensemble.tools.constants as CT


try:
    import win32com.client as com
    from pywintypes import com_error
except ModuleNotFoundError:
    click.echo(click.style("\t Platform non compatible with Windows", fg="yellow"))


class VissimConnector(object):
    """
        This models a connector and interactions from the API with the Vissim library.

        :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

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

    def load_scenario(self, scenario):
        """ checks existance and load scenario . Also get simulation parameters
        """
        if isinstance(scenario, VissimScenario):
            try:
                self._library.LoadNet(scenario.filename, scenario.bread_additional)
                self.sim_period = self._library.Simulation.AttValue('SimPeriod')
                self.sim_sec = self._library.Simulation.AttValue('SimSec')
                self.sim_res = self._library.Simulation.AttValue('SimRes')
                self.rand_seed = self._library.Simulation.AttValue('RandSeed')
                self.performInitialize(scenario)
                self.simulation = scenario
                click.echo(click.style(f"\t Scenario successfully loaded!", fg="green", bold=True))
                return
            except:
                raise EnsembleAPILoadFileError(f"\t Simulation network could not be loaded")
            try:
                self._library.LoadLayout(scenario.filename_layx)
                return
            except:
                raise EnsembleAPILoadFileError(f"\t Simulation layout could not be loaded")
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
        self.request.parse_data(vehsAttributes,self.sim_sec)

    def run_single_step(self):
        """ Run simulation next step

                :return: None
                :rtype: None
                """
        self._library.Simulation.RunSingleStep()

    def query_data(self) -> int:
        """ Run simulation step by step

        :return: iteration step
        :rtype: int
          To test query, you can use click.echo(self.get_vehicle_data()) after request_answer()
        """
        try:
            self.request_answer()
            #click.echo(self.get_vehicle_data())
            myvehids=self.request.get_vehicle_id()
            click.echo(myvehids)
            if len(myvehids)!=0:
                print(self.request.query_vehicle_data_dict('Acceleration', *myvehids))
                print(myvehids[-1],self.request.get_leader_id(myvehids[-1]))
                print(str(myvehids[0]), str(self.request.get_follower_id(myvehids[0])))
            self.run_single_step()
            self._c_iter = next(self._n_iter)
            return self._c_iter
        except StopIteration:
            self._bContinue = False
            return -1
    def push_update(self) -> None:
        """ Calls method within the Simulator request to
        """
        self.request.dispatch("VEHChannel")
    def get_vehicle_data(self):
        return self.request.get_vehicle_data().vehicles
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
       # self.request = SimulatorRequest()
        self.request = SimulatorRequest(
            ["VEHChannel", "FGCChannel", "RGCChannel"])
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

    def get_simulation_steps(self) -> range:
        """ Gets the list of simulation steps starting from 0 to end of simulation in step of simulation resolution"""
        return range(0,self.sim_period,self.sim_res)




