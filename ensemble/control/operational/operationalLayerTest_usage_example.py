# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 23:14:09 2020

@author: deschlen
"""
import numpy as np
from operationalLayerTest import operationalLayerTest
import matplotlib.pyplot as plt

olt = operationalLayerTest()
fleet = olt.runFullScenario()

fig, ax = plt.subplots(3, 1, sharex=True)
for vehicleNumber, vehicle in enumerate(fleet):
    ax[0].plot(vehicle.x)
    ax[1].plot(vehicle.v)
    ax[2].plot(vehicle.a)


plt.show()
