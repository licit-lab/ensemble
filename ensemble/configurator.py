import click
import ensemble.tools.constants as ct

from ensemble.handler.symuvia import SymuviaConnector, SymuviaScenario
from ensemble.handler.vissim.connector import VissimConnector, VissimScenario

from ensemble.control.tactical import MultiBrandPlatoonRegistry


class Configurator(object):
    """ 
        This class stores some simulation configurations. 
    """

    def __init__(self, verbose: bool = False) -> None:
        import platform

        self.verbose = verbose
        self.platform = platform.system()
        self.simulation_platform = ""
        self.scenario_files = []
        self.library_path = []
        self.simulation_parameters = ct.DCT_RUNTIME_PARAM

    def set_simulation_platform(self, simulation_platform: str = "") -> None:
        """ A simpler setter for the simulation platform based on OS

        :param simulation_platform: "symuvia" or "vissim", defaults to ""
        :type simulation_platform: str, optional
        """
        if simulation_platform:
            self.simulation_platform = simulation_platform
            return

        click.echo(click.style("Solving platform ", fg="blue", bold=True))

        self.simulation_platform = ct.DCT_SIMULATORS.get(self.platform, "")

        if self.verbose:
            click.echo(
                click.style(
                    f"Setting default simulation platform platform {(self.  simulation_platform, self.platform)}",
                    fg="yellow",
                )
            )

        self.library_path = ct.DCT_DEFAULT_PATHS.get((self.simulation_platform, self.platform))

        click.echo(click.style(f"Simulator path set to default value:\n \t {self.library_path}", fg="green",))
        return

    def update_values(self, **kwargs) -> None:
        """ Configurator updater, pass a with keyword arguments to update
        """

        if kwargs.get("library_path"):

            self.library_path = kwargs.get("library_path", self.library_path)

            click.echo(click.style(f"Setting new library path to user input:\n \t{self.library_path}", fg="yellow",))

        if kwargs.get("scenario_files"):
            self.scenario_files = kwargs.get("scenario_files", self.scenario_files)

            click.echo(
                click.style(f"Setting new scenario file(s) path to user input:  {self.library_path}", fg="yellow",)
            )

    def load_socket(self):
        """ Determines simulation platform to connect """
        if self.simulation_platform == "symuvia":
            self.connector = SymuviaConnector(self.library_path, stepLaunchMode="traj")
        else:
            self.connector = VissimConnector(self.library_path)

    def load_scenario(self):
        self.scenario_files = tuple(self.scenario_files)
        if self.simulation_platform == "symuvia":
            scenario = SymuviaScenario.create_input(*self.scenario_files)  # expected input (fileA,fileB)
        else:
            scenario = VissimScenario.create_input(*self.scenario_files)  # expected input (fileA,fileB)

        # Call connector (automatic dispatch)
        self.connector.load_scenario(scenario)

    def query_data(self):
        self.connector.query_data()

    def create_platoon_registry(self):
        """ Creates a platoon registry for all coordinators (FGC-RGC) """
        self.platoon_registry = MultiBrandPlatoonRegistry()

    def update_platoon_registry(self):
        if hasattr(self, "platoon_registry"):
            self.connector.push_update()
            return
        self.create_platoon_registry()

    @property
    def total_steps(self):
        return self.simulation_parameters.get("total_steps")
