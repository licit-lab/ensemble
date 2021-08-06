"""
Reference Control
=================

This model is here to create the reference for the operational controller based on a specific time window.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ensemble.component.dynamics import TIME_STEP
import numpy as np
from typing import Iterable, Iterator
from functools import partial
from dataclasses import dataclass
import matplotlib.pyplot as plt

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.metaclass.state import AbsState
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)

from ensemble.tools.constants import DCT_RUNTIME_PARAM, DCT_PLT_CONST, TIME_STEP

TIME_STEP_OP = DCT_RUNTIME_PARAM["sampling_time_operational"]
TIME_INTERVAL = DCT_RUNTIME_PARAM["sampling_time_tactical"]
TIME_GAP = DCT_PLT_CONST["time_gap"]
CRUISE_SPEED = DCT_PLT_CONST["cruise_speed"]

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class ReferenceHeadway:
    """This is a class to model the reference for a controller, consume, regenerate trajectory, plot trajectory.

    The maneuvers are planned on a horizon of 60 seconds and the references are created on streams of 1 second. Each stream once consummed exams the status before generating a new sequence.
    """

    sim_step: float = TIME_STEP
    time_step: float = TIME_STEP_OP
    interval: float = TIME_INTERVAL
    gap0: float = TIME_GAP
    gapT: float = TIME_GAP
    v0: float = CRUISE_SPEED
    VT: float = CRUISE_SPEED
    current_gap: float = TIME_GAP
    current_speed: float = CRUISE_SPEED
    current_time: float = 0

    def __iter__(self):
        self.count = 0
        self.chunk_space = iter(next(self.chunks_space))
        self.chunk_speed = iter(next(self.chunks_speed))
        self.time_running = iter(next(self.time_chunks))
        return self

    def __next__(self):
        self.count += 1
        if self.count <= int(self.sim_step / self.time_step):
            self.current_gap = next(self.chunk_space)
            self.current_speed = next(self.chunk_speed)
            self.current_time = next(self.time_running)
            return self.current_time, self.current_gap, self.current_speed
        else:
            raise StopIteration

    def create_time_gap_hwy(self, state: AbsState):
        """Creates an array containing the time gap reference for an interval of time based on the state of the vehicle gap.

        Args:
            state (AbsState): State of the platoon

        Returns:
            Iterable: Iterable array containing time gap values.
        """

        self.horizon = np.arange(0, self.interval, self.time_step)

        if isinstance(state, Platooning) or isinstance(state, Joining):
            self.gap0 = self.current_gap
            self.gapT = TIME_GAP
            self.v0 = self.current_speed
            self.VT = CRUISE_SPEED

        if isinstance(state, Splitting):
            self.gap0 = self.current_gap
            self.gapT = 3 * TIME_GAP
            self.v0 = self.current_speed
            self.VT = CRUISE_SPEED

        self.reference_headway = ReferenceHeadway.change_time_gap(
            self.horizon,
            self.gap0,
            self.gapT,
        )
        self.reference_cruise = ReferenceHeadway.change_time_gap(
            self.horizon,
            self.v0,
            self.VT,
        )

        self.chunks_space = iter(
            np.array_split(
                self.reference_headway,
                int(self.interval / self.sim_step),
            )
        )
        self.chunks_speed = iter(
            np.array_split(
                self.reference_cruise,
                int(self.interval / self.sim_step),
            )
        )
        self.time_chunks = iter(
            np.array_split(
                self.horizon + self.current_time,
                int(self.interval / self.sim_step),
            )
        )

    @staticmethod
    def sigmoid(x, A: float = 1, a: float = 5, d: int = 30) -> np.ndarray:
        """Sigmoid function"""
        return A * 1 / (1 + np.exp(-(x - d) / a))

    @staticmethod
    def change_time_gap(
        time_vector: np.ndarray,
        T0: float = TIME_GAP,
        TF: float = TIME_GAP,
    ) -> np.ndarray:
        """Create a decreasing jump on speed"""
        delta = TF - T0
        vector = ReferenceHeadway.sigmoid(time_vector, A=delta)
        return T0 + vector

    def plot_case(self, state: AbsState):
        self.create_time_gap_hwy(state)
        _, a = plt.subplots(2, 1)
        a[0].plot(self.horizon, self.reference_headway)
        a[0].set_ylabel("Time Gap [s]")
        a[0].grid()
        a[1].plot(self.horizon, self.reference_cruise)
        a[1].set_ylabel("Cruise speed [m/s]")
        a[1].grid()
        plt.xlabel("Time[s]")
        plt.show()


if __name__ == "__main__":
    r = ReferenceHeadway()
    # r.plot_case(Splitting())
    c = ["r", "b"]

    _, a = plt.subplots(2, 1)
    r.create_time_gap_hwy(Splitting())
    for j in range(30):
        for t, x, v in r:
            a[0].scatter((t,), (x,), color="red")
            a[1].scatter((t,), (v,), color="red")

    r.create_time_gap_hwy(Splitting())
    for j in range(60):
        for t, x, v in r:
            a[0].scatter((t,), (x,), color="blue")
            a[1].scatter((t,), (v,), color="blue")

    r.create_time_gap_hwy(Joining())
    for j in range(60):
        for t, x, v in r:
            a[0].scatter((t,), (x,), color="orange")
            a[1].scatter((t,), (v,), color="orange")

    r.create_time_gap_hwy(Platooning())
    for j in range(60):
        for t, x, v in r:
            a[0].scatter((t,), (x,), color="green")
            a[1].scatter((t,), (v,), color="green")

    plt.show()
