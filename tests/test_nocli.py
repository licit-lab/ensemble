from ensemble.ensemble import launch_simulation
from ensemble.configurator import Configurator
import os

from ensemble.tools.constants import DEFAULT_PATH_SYMUVIA

bottleneck04 = os.path.join(
    os.getcwd(), "tests", "mocks", "bottlenecks", "bottleneck_004.xml"
)


c = Configurator()
c.set_simulation_platform("")  # Automatic detection
c.update_values(scenario_files=(bottleneck04,))  # Set scenario

if __name__ == "__main__":
    launch_simulation(c)
