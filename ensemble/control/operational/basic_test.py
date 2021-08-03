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
from ensemble.control.operational.reference import ReferenceHeadway

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

    ## Controller, vehicles
    cacc = CACC()
    request = SymuviaRequest()  # Dummy publisher
    vehlist = VehicleList(request)
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

    ggc = GlobalGapCoordinator(vehlist)
    ggc.attach_control(cacc)

    # Runtime
    sim_time = 60  # [s]

    for i in range(3):

        # Get couple of states
        list_bi_states = []
        for lead, follow in zip(list_vehicles[:-2], list_vehicles[1:]):
            leader = {
                "x": lead.distance,
                "v": lead.speed,
                "a": lead.acceleration,
            }
            follower = {
                "x": follow.distance,
                "v": follow.speed,
                "a": follow.acceleration,
                "PV": lead.speed - follow.speed,
            }
            list_bi_states.append((leader, follower))

        # compute control
        u = []
        for v in vehlist:
            a = cacc(ggc[v].leader, ggc[v])
            u.append(a)

        # apply control
        for v, control in zip(vehlist, u):
            v.dynamics(control)


if __name__ == "__main__":
    import os

    cacc_path = os.path.join(
        os.getcwd(), "ensemble", "libs", "darwin", "OperationalDLL.dylib"
    )
    truck_path = os.path.join(
        os.getcwd(), "ensemble", "libs", "darwin", "truckDynamics.dylib"
    )

    # Initial condition
    X0 = np.array([[0, 25], [30, 26]])
    runtime_op_layer(X0)
