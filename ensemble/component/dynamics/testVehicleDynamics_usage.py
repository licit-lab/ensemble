# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 21:42:59 2021

@author: deschlen
"""
import numpy as np
from testVehicleDynamics import testVehicleDynamics
import matplotlib.pyplot as plt
from scipy import stats
from numpy import random
#%% Run one time step for testing
tvd = testVehicleDynamics()
tvd.resetParameters()
x=0
v=25
a=0
vid=88
x,v,a = tvd.runOnePoint(
        vid=vid,
        a_r=10,
        x=x,
        v=v,
        a=a,)
#%% Run for T timesteps
T = 300
tvd = testVehicleDynamics()
tvd.resetParameters()
x=0
v=0
a=0
vid=88
vss=[]
ass=[]
for i in range(T):
    x,v,a = tvd.runOnePoint(
        vid=vid,
        a_r=.5,
        v=v,)
    ass.append(a)
    vss.append(v)
vss = np.array(vss)
f,a = plt.subplots(2,1)
a[0].plot(vss,'.')
a[0].set_ylabel('Velocity')
a[1].plot(ass,'.')
a[1].set_ylabel('Acceleration')
a[0].set_xlabel('Time step')
a[1].set_xlabel('Time step')
#plt.plot(np.diff(vss),'.')
# vid += 1
#%% See a scenario
tvd = testVehicleDynamics()
tvd.resetParameters()
tvd.defineAndRunOneScenario(accel=4,vid=88)
time = np.arange(0,tvd.xSeriesOut.shape[0]*.1,.1)
fig, (ax2,ax1) = plt.subplots(1,2,sharex=True, gridspec_kw={'width_ratios': [1, 2.5]})
ax1.plot(time,tvd.aSeriesOut,'.-',markersize=6.5)
ax2.plot(time,tvd.vSeriesOut*3.6,'.',markersize=6.5)
ax2.set_xlim([0,80])
ax2.set_xticks(np.arange(0,90,10))
# ax1.set_yticks(np.arange(0,.6,.1))
ax2.set_yticks(np.arange(0,110,20))
ax2.set_ylim([0,100])
ax2.grid()
ax1.grid()
ax2.set_xlabel('Time [s]')
ax1.set_ylabel('Acceleration [m/s^2]')
ax2.set_ylabel('Velocity [km/h]')
#%% See compltete module behavior plotting the a vs v curve
tvd = testVehicleDynamics()
#tvd.defineAndRunScenarios()
# tvd.defineAndRunOneScenario()
tvd.defineAndRunRandomScenario( maxF = .051/(2*np.pi),
                                   maxA = 10000,
                                   reps = 100,)
# tvd.plotScenario()

o=000;i=o+000;j=o+18000;
# plt.plot(tvd.vSeriesOut[i:j],tvd.aSeriesOut[i:j],'.')
plt.plot(tvd.vSeriesOut,tvd.aSeriesOut,'.')
plt.ylim([0,3.5])
plt.xlabel('Velocity [m/s]')
plt.ylabel('Acceleration [m/s^2]')
#%% Plot also accel
plt.plot(tvd.aSeries,'.',label='ain')
plt.plot(tvd.aSeries,'-',label='ain')
plt.legend()
#%%
plt.plot(tvd.aSeriesOut,'.',label='aout')
plt.plot(tvd.vSeriesOut,'.',label='vout')
plt.xlim([4000,4500])
plt.legend()
# tvd.plotScenario(save=False,show=True)
#%%
tvd = testVehicleDynamics()
# tvd.defineAndRunScenarios()
tvd.computeAccelerationMass(maxF = .051/(2*np.pi),
                            maxA = 10000,
                            reps = 100,)
# tvd.plotScenario()


o=000;i=o+000;j=o+18000;
# plt.plot(tvd.vSeriesOut[i:j],tvd.aSeriesOut[i:j],'.')
fig = plt.figure()
ax = fig.add_subplot()
ax.plot(np.array(tvd.allMasses).astype(int),np.array(tvd.allMaxAccel),'.')
ax.get_yaxis().get_major_formatter().set_useOffset(False)
ax.set_xlabel('Mass [kg]')
ax.set_ylabel('Max(a) [m/s^2]')
plt.ylim([3,4])
# ax.plot(tvd.allMasses,tvd.allMeanAccel,'.')
#%%
for i in range(45,len(tvd.alla)):
    plt.plot(tvd.allv[i],tvd.alla[i],'.')
plt.ylim([0,3.5])
plt.xlabel('Velocity [m/s]')
plt.ylabel('Acceleration [m/s^2]')