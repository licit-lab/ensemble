from ensemble.ensemble import launch_simulation
from ensemble.configurator import Configurator
import os
import sys

bottleneck04 = os.path.join(
    os.getcwd(), "tests", "mocks", "symuvia", "bottleneck_004.xml"
)

file_path = ("tests", "mocks", "vissim", "TestNetwork.inpx")
file_layx_path = ("tests", "mocks", "vissim", "TestNetwork.layx")

c = Configurator()
c.set_simulation_platform("")  # Automatic detection
if c.platform == "Darwin":
    c.update_values(scenario_files=(bottleneck04,))  # Set scenario
else:
    c.update_values(scenario_files=(file_path, file_layx_path))  # Set scenario

if __name__ == "__main__":
    launch_simulation(c)
