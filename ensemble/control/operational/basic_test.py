# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from matplotlib.colors import LinearSegmentedColormap
from networkx.readwrite.gml import escape
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
            dyn_path=DEFAULT_TRUCK_PATH,
            distance=x0[0],
            abscissa=x0[0],
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
    sim_time = 300  # [s]

    for t in range(sim_time):
        print(t)
        ggc.apply_cacc(t)

    return ggc


if __name__ == "__main__":

    # Initial condition
    X0 = np.array([[80, 25], [60, 26], [40, 25], [20, 10]])
    ggc = runtime_op_layer(X0)

    X = np.vstack([ggc[i].history_state[:, 0] for i in range(4)]).T
    V = np.vstack([ggc[i].history_state[:, 1] for i in range(4)]).T
    A = np.vstack([ggc[i].history_state[:, 2] for i in range(4)]).T
    S = np.vstack(
        [
            ggc[i].history_state[:, 0] - ggc[i + 1].history_state[:, 0]
            for i in range(3)
        ]
    ).T

    ES = np.vstack(
        [
            ggc[i].history_reference[:, 2] * V[:, i] - S[:, i - 1]
            for i in range(1, 4)
        ]
    ).T

    EV = np.vstack(
        [ggc[i].history_reference[:, 1] - V[:, i] for i in range(4)]
    ).T

    from matplotlib import pyplot as plt
    import numpy as np

    t = ggc[0].history_reference[:, 0]
    fig, ax = plt.subplots(1, 4, figsize=(20, 5))
    ax[0].plot(t, X, label="Position [m]")
    ax[1].plot(t, V, label="Speed [m/s]")
    ax[2].plot(t, A, label="Acceleration [m/s2]")
    ax[3].plot(t, S, label="Headway Space [m]")
    [a.grid() for a in ax]
    [a.set_xlabel("Time [s]") for a in ax]
    [
        a.set_ylabel(b)
        for a, b in zip(
            ax,
            (
                "Position $x_i[m]$",
                "Speed $v_i[m/s]$",
                "Acceleration $a_i[m/s^2]$",
                "Space Headway $(x_{i-1}-x_i)[m]$",
            ),
        )
    ]
    plt.tight_layout()

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].plot(t, ES, label="Position [m]")
    ax[1].plot(t, EV, label="Speed [m/s]")
    [a.grid() for a in ax]
    [a.set_xlabel("Time [s]") for a in ax]
    [
        a.set_ylabel(b)
        for a, b in zip(
            ax,
            (
                "Error Headway space \n "
                + r"$ e_s = \tau_g *v_i - (x_{i-1}-x_{i}) - [m]$",
                "Error Speed \n  $e_v = r_{v_i} - v_i - [m/s]$",
            ),
        )
    ]
    plt.tight_layout()
    plt.show()

    ggc
