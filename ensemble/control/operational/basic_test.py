# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.screen import log_verify
from ensemble.control.operational import CACC
from ensemble.component.dynamics import TruckDynamics

from ensemble.handler.symuvia.stream import SimulatorRequest as SymuviaRequest
from ensemble.component.vehiclelist import VehicleList
from ensemble.component.platoon_vehicle import PlatoonVehicle
from ensemble.control.tactical.gapcordinator import GlobalGapCoordinator

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

from ensemble.tools.constants import (
    DEFAULT_CACC_PATH,
    DEFAULT_TRUCK_PATH,
    DCT_RUNTIME_PARAM,
)


def runtime_op_layer(initial_condition: np.ndarray, scenario: str = "platoon"):
    """Basic test runtime operational layer"""

    log_verify(f"Test: {scenario}")

    # Controller
    cacc = CACC()

    # Vehicle
    request = SymuviaRequest()  # Dummy publisher
    vehlist = VehicleList(request)

    # Sintetic vehicle data
    for i, x0 in enumerate(initial_condition):
        vehicle = PlatoonVehicle(
            request,
            vehid=i,
            vehtype="PLT",
            dyn_path=truck_path,
            distance=x0[0],
            speed=x0[1],
        )
        vehlist.update_list(
            extra=[
                vehicle,
            ]
        )

    # Creating the platoon
    ggc = GlobalGapCoordinator(vehlist)
    ggc.cacc = cacc

    # Runtime evolution
    sim_time = 60  # [s]

    for t in range(sim_time):
        ggc.apply_cacc(t)


if __name__ == "__main__":
    import os

    cacc_path = os.path.join(
        os.getcwd(), "ensemble", "libs", "darwin", "OperationalDLL.dylib"
    )
    truck_path = os.path.join(
        os.getcwd(), "ensemble", "libs", "darwin", "truckDynamics.dylib"
    )

    # Initial condition
    X0 = np.array([[30, 25], [0, 26]])
    runtime_op_layer(X0)
