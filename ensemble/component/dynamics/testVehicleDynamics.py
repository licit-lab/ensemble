# import os
# import sys
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint
from numpy.random import random
import platform

        
class testVehicleDynamics():
    def __init__(self,
                 ):
        if platform.system() == 'Windows':
            print('Running on win')
            file_dll = './truckDynamics.dll'
        elif platform.system() == 'Darwin':
            print('Running on mac')
            file_dll = './truckDynamics.dylib'
        print('Using {}...'.format(file_dll),flush=True)
        self.lib = ctypes.cdll.LoadLibrary(file_dll)
        self.id = ctypes.c_double(0)
        self.resetParameters()

    def resetParameters(self,
                        ):
        self.requestedAcceleration = ctypes.c_double(0)
        self.x = ctypes.c_double(0)
        self.v = ctypes.c_double(0)
        self.a = ctypes.c_double(0)
        self.interAxes = ctypes.c_double(.75)
        self.long = ctypes.c_double(5.92)
        self.width = ctypes.c_double(2.49)
        self.mass = ctypes.c_double(26450.0)

    def setMass(self,
                mass = 26450.0):
        self.mass = ctypes.c_double(mass)

    def clearState(self,
                   ):
        pass

    def defineScenario(self,
                       T,
                       aPar,
                       sCode):
        dt = .1
        if sCode == 1:
            aSeries = []
            scenario = '{}_T{}_constant{:.2f}'.format(sCode,T,aPar[0])
            for ii in range(T):
                aSeries.append(aPar)
        if sCode == 2:
            aSeries = []
            aPar = np.array(aPar)
            scenario = '{}_T{}_accel{:.2f}_decel{:.2f}'.format(sCode,T,aPar[0],aPar[1])
            for ii in range(round(T-T/10)):
                aSeries.append(aPar[0])
            for ii in range(round(T/10)):
                aSeries.append(aPar[1])
        if sCode == 3:
            aSeries = []
            aPar = np.array(aPar)
            scenario = '{}_T{}_accel{:.2f}_sth{:.2f}_sth{:.2f}'.format(sCode,T,aPar[0],aPar[1],aPar[2])
            for ii in range(round(T*.4)):
                aSeries.append(aPar[0])
            for ii in range((round(T*.2))):
                aSeries.append(aPar[1])
            for ii in range((round(T*.4))):
                aSeries.append(aPar[2])
        if sCode == 4:
            aSeries = []
            aPar = np.array(aPar)
            a = 0;
            scenario = '{}_T{}_jerk{:.2f}_stop_dejerk{:.2f}'.format(sCode,T,aPar[0],aPar[1])
            for ii in range(round(T*.4)):
                a = a + aPar[0]*dt
                aSeries.append(a)
            for ii in range((round(T*.2))):
                a = a
                aSeries.append(a)
            for ii in range((round(T*.4))):
                a = a + aPar[1]*dt
                aSeries.append(a)
        self.scenario = scenario
        self.aSeries = np.array(aSeries)

    def makeC(self,
              x = None,
              ctype = None,
              ):
        if x is None:
            if ctype is None:
                return ctypes.c_double()
            else:
                return ctypes.c_int()
        else:
            if ctype is None:
                return ctypes.c_double(x)
            else:
                return ctypes.c_int(x)

    def runOnePoint(self,
                    vid = None,
                    a_r = None,
                    x = None,
                    v = None,
                    a = None,
                    ia = None,
                    l = None,
                    w = None,
                    m = None,):
        vid = self.makeC(vid,ctype='integer')
        a_r = self.makeC(a_r)
        x = self.makeC(x)
        v = self.makeC(v)
        a = self.makeC(a)
        ia = self.makeC(ia)
        l = self.makeC(l)
        w = self.makeC(w)
        m = self.makeC(m)
        try:
            self.lib.TruckDynamics_dll(
                vid,
                a_r,
                ctypes.byref(x),
                ctypes.byref(v),
                ctypes.byref(a),
                ctypes.byref(ia),
                ctypes.byref(l),
                ctypes.byref(w),
                ctypes.byref(m),
                )
            print('x:{:.3f}, v:{:.3f}, a:{:.3f}'.format(x.value,v.value,a.value))
            return x.value,v.value,a.value
        except ValueError:
            print('Calling dll failed.')

    def runScenario(self,
                    vehicleID = 0,
                    ):
        xSeriesOut = []
        vSeriesOut = []
        aSeriesOut = []
        for iii in range(self.aSeries.shape[0]):
            self.requestedAcceleration = ctypes.c_double(self.aSeries[iii])
            try:
                self.lib.TruckDynamics_dll(
                    ctypes.c_int(vehicleID),
                    self.requestedAcceleration,
                    ctypes.byref(self.x),
                    ctypes.byref(self.v),
                    ctypes.byref(self.a),
                    ctypes.byref(self.interAxes),
                    ctypes.byref(self.long),
                    ctypes.byref(self.width),
                    ctypes.byref(self.mass),
                    )
            except:
                print('Calling dll failed.')
            # if iii > 60/.1:
            #     print(self.a.value)
            xSeriesOut.append(self.x.value)
            vSeriesOut.append(self.v.value)
            aSeriesOut.append(self.a.value)

        self.xSeriesOut = np.array(xSeriesOut)
        self.vSeriesOut = np.array(vSeriesOut)
        self.aSeriesOut = np.array(aSeriesOut)

    def plotScenario(self,
                     save = True,
                     show = False,
                     ):
        my_dpi = 100
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1,
                                            sharex = True,
                                            figsize = (800/my_dpi, 00/my_dpi),
                                            dpi = my_dpi)
        time = np.arange(0,self.xSeriesOut.shape[0]*.1,.1)
        ax1.plot(time, self.xSeriesOut,'.-')
        ax1.set_title('Position')
        ax1.set_ylabel('Position [m]')
        ax2.plot(time, self.vSeriesOut,'.-')
        ax2.set_title('Velocity')
        ax2.set_ylabel('Velocity [m/s]')
        ax3.plot(time, self.aSeriesOut,'.-')
        ax3.plot(time, self.aSeries, '-', label='Requested acceleration')
        ax3.set_title('Acceleration')
        ax3.set_ylabel('Acceleration [m/s^2]')
        ax3.set_xlabel('Time [s]')
        ax3.axhline(y=0, linewidth=2, color='r', linestyle='--')
        ax3.legend()
        if save:
            fig.savefig('output/truckDynamics_scenario_{}.png'.format(self.scenario),format='png',dpi=300)
        if show:
            fig.show()
        plt.close('all')

    def plotAcceleratioVelocityCurve(self,
                                     ylim1 = 0,
                                     ylim2 = 3.5,
                                     ):
        plt.plot(self.vSeriesOut,self.aSeriesOut,'.')
        plt.ylim([ylim1,ylim2])
        plt.xlabel('Velocity [m/s]')
        plt.ylabel('Acceleration [m/s^2]')
        plt.savefig('output/a_vs_v.png',format='png')
        plt.close('all')

    def defineAndRunRandomScenario(self,
                                   maxF = .051/(2*np.pi),
                                   maxA = 10000,
                                   reps = 100,
                                   ):
        self.scenario = 'random'
        x = []
        t_ = np.arange(0,100,.1)
        for i in range(reps):
            # x.extend(list(np.convolve(randint(0,maxF)*np.sin(randint(0,maxF)*t_), randint(0,maxF)*np.cos(randint(0,maxF)*t_), 'same')))
            # x.extend(list(randint(0,maxA)*np.sin(randint(0,maxF)*t_)+randint(0,maxA)*np.cos(randint(0,maxF)*t_)))
            x.extend(list(random()*maxA*np.sin(random()*maxF*2*np.pi*t_)+random()*maxA*np.cos(random()*maxF*2*np.pi*t_)))
        x = np.array(x)
        self.aSeries = x
        self.runScenario(vehicleID = 6)
        # self.plotScenario()

    def computeAccelerationMass(self,
                                maxF = .051/(2*np.pi),
                                maxA = 10000,
                                reps = 100,
                                ):
        self.allMasses = []
        self.allv = []
        self.alla = []
        self.allMaxAccel = []
        self.allMeanAccel = []
        for mass in np.arange(5000,self.mass.value*2,1000):
            self.setMass(mass)
            self.defineAndRunRandomScenario()
            # self.allv.append(self.vSeriesOut)
            # self.alla.append(self.aSeriesOut)
            self.allMasses.append(self.mass.value)
            self.allMaxAccel.append(np.max(self.aSeriesOut))
            self.allMeanAccel.append(np.mean(self.aSeriesOut))


    def defineAndRunOneScenario(self,
                                accel = None,
                                duration = 50000,
                                vid = 0,
                                ):
        counter = vid
        if type(accel) is not type([]) and type(accel) is not type(np.array([])):
            accel = [accel]
        if type(duration) is not type([]) and type(duration) is not type(np.array([])):
            duration = [duration]
        for tt in duration:
            for acel in accel:#np.arange(.1,1,.2):
                # self.clearState()
                self.defineScenario(T=tt,aPar=[acel],sCode=1)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                # self.plotScenario()

    def defineAndRunScenarios(self,
                              ):
        counter = 0
        for tt in [100]:
            for acel in np.arange(.1,1,.2):
                # clearState()
                self.defineScenario(T=tt,aPar=[acel],sCode=1)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                self.plotScenario()

        for tt in [600,1000]:
            for acel in np.arange(.1,2,.2):
                # self.clearState()
                self.defineScenario(T=tt,aPar=[acel,-acel],sCode=2)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                self.plotScenario()

        for tt in [100,1000]:
            for acel in np.arange(.1,2,.2):
                # clearState()
                self.defineScenario(T=tt,aPar=[acel,0,-acel],sCode=3)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                self.plotScenario()

        for tt in [100,1000]:
            for acel in np.arange(.1,2,.2):
                # clearState()
                self.defineScenario(T=tt,aPar=[acel,-acel,acel],sCode=3)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                self.plotScenario()

        for tt in [300,1000]:
            for acel in np.arange(.1,.8,.2):
                # clearState()
                self.defineScenario(T=tt,aPar=[acel,-acel],sCode=4)
                self.resetParameters()
                self.runScenario(vehicleID = counter)
                counter += 1
                self.plotScenario()

def main():
    tvd = testVehicleDynamics()
    # tvd.defineAndRunScenarios()
    tvd.defineAndRunOneScenario()
    # tvd.defineAndRunRandomScenario()
    # tvd.plotScenario()

if __name__ == '__main__':
    main()

