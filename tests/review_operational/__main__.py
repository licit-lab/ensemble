from vehicles import System, Integrator, RegularVehicle
from operational import CACC
from pid import PID

import numpy as np
import pandas as pd

#%%
HWY = 20
T = 0.1
X0 = HWY
T0 = RegularVehicle(X0, 0, 0, T=T)

r0_v = np.concatenate(
    [
        np.zeros(400),
        1 / 1000 * np.cumsum(np.ones(1000)),
        np.ones(1000),
        1 - 1 / 1000 * np.cumsum(np.ones(1000)),
        np.zeros(250),
    ]
)
r0_x = np.cumsum(r0_v) + X0

#%%
# Control
pid_v = PID(k_p=0.005, k_i=0, k_d=0, T=T)
e_v = []

for r_v, r_x in zip(r0_v, r0_x):

    #     err_v = r_v-T0.v
    err_x = r_x - T0.x
    e_v.append(err_x)
    ctr0 = pid_v(err_x)  # Leader
    T0(ctr0)
