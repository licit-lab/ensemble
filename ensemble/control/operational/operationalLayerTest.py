import os
import ctypes
ERROR_CODE = -1
import numpy as np

class oem(object):
    def __init__(self,
                 ):
        self.a = []
        self.v = []
        self.x = []

class operationalLayerTest():
    def __init__(self,):
        self.loadingSucceded = False
        self.loadLib()
        # self.lead_speed_ts = []
        # self.lead_accel_ts = []
        # self.lead_position_ts = []
        # self.veh_speed_ts = []
        # self.veh_accel_ts = []
        # self.veh_position_ts = []
        self.testDurationInSeconds = 600
        if self.loadingSucceded:
            self.initializePars()
        self.veh_autonomous_operational_acceleration = ctypes.c_double(0)
        self.veh_autonomous_operational_mixingmode = ctypes.c_long(1)
        self.veh_autonomous_operational_warning = ctypes.c_double(1)
        self.veh_cc_setpoint = ctypes.c_double(1)
        self.veh_cruisecontrol_acceleration = ctypes.c_double(1)
        self.success = ctypes.c_int(0)
        self.initializePars()
        self.sPars = dict()

    def run(self,):
        self.call()
        self.printOutput()

    def loadLib(self,):
        import platform
        import sys
        if platform.system() == 'Windows':
            print('Running on win')
            file_dll = '../x64/Debug/OperationalDLL.dll'
        elif platform.system() == 'Darwin':
            print('Running on mac')
            file_dll = 'OperationalDLL.dylib'
        else:
            print('System not supported')
            sys.exit()

        # Load operational DLL
        self.lib = None
        try:
            self.lib = ctypes.cdll.LoadLibrary(file_dll)
            self.loadingSucceded = True
        except:
            print('Error: DLL file could not be found')

    def initializePars(self,):
        self.varDict = {'curr_lead_veh_acceleration':2.0,
        'curr_lead_veh_id':40,
        'curr_lead_veh_rel_velocity':-1.0,
        'curr_lead_veh_type':10,
        'curr_timestep':55.0,
        'curr_ts_length':.1,
        'curr_veh_id':10,
        'curr_veh_setspeed':88/3.6,
        'curr_veh_type':10,
        'curr_veh_controller_in_use':10,
        'curr_veh_ACC_h':1.6,
        'curr_veh_CACC_h':.6,
        'curr_veh_used_distance_headway':20.0,
        'curr_veh_used_rel_vel':-1.0,
        'curr_veh_velocity':85./3.6,
        'curr_veh_autonomous_operational_warning':10,
        'curr_veh_platooning_max_acceleration':2.0,
        'prev_veh_cc_setpoint':85./3.6,
        'prev_veh_cruisecontrol_acceleration':2.0,
        'prev_veh_distance_headway':20.0,
        'prev_veh_executed_acceleration':-2.0}
    def setMetaPars(self,
                    ):
        self.sPars['v0'] = 32
        self.sPars['lead_position'] = 100

    def setPars(self,
                scenario = 'stop-go'):
        self.varDict['curr_lead_veh_acceleration'] = 0 #SET
        self.varDict['curr_lead_veh_id'] = 1
        self.varDict['curr_lead_veh_rel_velocity'] = 0 #--> observed
        self.varDict['curr_lead_veh_type'] = 1 #

        self.varDict['curr_timestep'] = 0
        self.varDict['curr_ts_length'] = .1

        self.varDict['curr_veh_id'] = 2

        self.varDict['curr_veh_setspeed'] = 32 #--> this is important!

        self.varDict['curr_veh_type'] = 1
        self.varDict['curr_veh_controller_in_use'] = 2 # acc 1 cacc 2
        self.varDict['curr_veh_ACC_h'] = 1.6 # [s]
        self.varDict['curr_veh_CACC_h'] = .6

        self.varDict['curr_veh_used_rel_vel'] = self.varDict['curr_lead_veh_rel_velocity'] #--> delayed for ACC
        #this
        self.varDict['curr_veh_velocity'] = self.sPars['v0'] # m/s!
        self.varDict['curr_veh_autonomous_operational_warning'] = 0 #0
        self.varDict['curr_veh_platooning_max_acceleration'] = 1 #2

        self.varDict['prev_veh_cc_setpoint'] = 32
        self.varDict['prev_veh_cruisecontrol_acceleration'] = 0 # to prevent jerk

        self.lead_speed = self.varDict['curr_veh_velocity'] - self.varDict['curr_lead_veh_rel_velocity']
        self.varDict['curr_veh_used_distance_headway'] = (
            self.varDict['curr_veh_velocity'] * self.varDict['curr_veh_ACC_h'] + 2
            ) #
        self.varDict['prev_veh_distance_headway'] = self.varDict['curr_veh_used_distance_headway']
        self.lead_position = self.sPars['lead_position']
        self.veh_length = 4
        self.veh_position = self.lead_position - self.varDict['curr_veh_used_distance_headway'] - self.veh_length
        if scenario == 'cut-in':
             self.veh_position -= self.sPars['extraGap']

        self.varDict['prev_veh_executed_acceleration'] = 0 #

    def setAloneScenario(self,):
        self.varDict['curr_lead_veh_acceleration'] = 999 #SET
        self.varDict['curr_lead_veh_id'] = 1
        self.varDict['curr_lead_veh_rel_velocity'] = 0 #--> observed
        self.varDict['curr_lead_veh_type'] = 999 #

        self.varDict['curr_timestep'] = 0
        self.varDict['curr_ts_length'] = .1

        self.varDict['curr_veh_id'] = 2

        self.varDict['curr_veh_setspeed'] = 32 #--> this is important!

        self.varDict['curr_veh_type'] = 1
        self.varDict['curr_veh_controller_in_use'] = 2 # acc 1 cacc 2
        self.varDict['curr_veh_ACC_h'] = 1.6 # [s]
        self.varDict['curr_veh_CACC_h'] = .6

        self.varDict['curr_veh_used_rel_vel'] = 0 #--> delayed for ACC
        #this
        self.varDict['curr_veh_velocity'] = 32 # m/s!
        self.varDict['curr_veh_autonomous_operational_warning'] = 0 #0
        self.varDict['curr_veh_platooning_max_acceleration'] = 1 #2

        self.varDict['prev_veh_cc_setpoint'] = 32
        self.varDict['prev_veh_cruisecontrol_acceleration'] = 0 # to prevent jerk
        self.varDict['prev_veh_executed_acceleration'] = 0 #

        self.lead_speed = self.varDict['curr_veh_velocity'] - self.varDict['curr_lead_veh_rel_velocity']
        self.varDict['curr_veh_used_distance_headway'] = (
            self.varDict['curr_veh_velocity'] * self.varDict['curr_veh_ACC_h'] + 2
            ) #
        self.varDict['prev_veh_distance_headway'] = self.varDict['curr_veh_used_distance_headway']
        self.lead_position = 100
        self.veh_length = 4
        self.veh_position = self.lead_position - self.varDict['curr_veh_used_distance_headway'] - self.veh_length

        deltat = self.varDict['curr_ts_length']
        self.time = np.arange(0,self.testDurationInSeconds,deltat)
        lead_accel = self.varDict['curr_lead_veh_acceleration']
        lead_speed = self.lead_speed
        lead_position = self.lead_position
        for t in self.time:
            self.lead_speed_ts.append(lead_speed)
            self.lead_accel_ts.append(lead_accel)
            self.lead_position_ts.append(lead_position)
        self.lead_speed_ts = np.array(self.lead_speed_ts)
        self.lead_accel_ts = np.array(self.lead_accel_ts)
        self.lead_position_ts = np.array(self.lead_position_ts)

    def defineLeaderProfile(self,
                            scenario = 'stop-go'):
        vehicle = oem()
        self.setPars(scenario=scenario)
        stopTime = 0
        interval = 50
        #initial values
        deltat = self.varDict['curr_ts_length']
        lead_accel = self.varDict['curr_lead_veh_acceleration']
        lead_speed = self.lead_speed
        lead_position = self.lead_position
        self.time = np.arange(0,self.testDurationInSeconds,deltat)
        speed_ts = []
        accel_ts = []
        position_ts = []
        #evolved values
        if scenario == 'stop-go':
            for t in self.time:
                if t == interval:
                    lead_accel = -9.8/80
                if t > interval and lead_accel == -9.8/80 and lead_speed <= 0:
                    lead_accel = 0
                    stopTime = t
                if t > interval and lead_accel == 0 and (t-stopTime) > interval:
                    lead_accel = 9.8/80
                lead_speed = lead_speed + lead_accel * deltat
                lead_position = (
                    + lead_position
                    + lead_speed * deltat
                    + .5 * lead_accel * deltat**2
                    )
                speed_ts.append(lead_speed)
                accel_ts.append(lead_accel)
                position_ts.append(lead_position)
        elif scenario == 'cut-in':
            for t in self.time:
                lead_position = (
                    + lead_position
                    + lead_speed * deltat
                    + .5 * lead_accel * deltat**2
                    )
                speed_ts.append(lead_speed)
                accel_ts.append(lead_accel)
                position_ts.append(lead_position)
        vehicle.v = np.array(speed_ts)
        vehicle.a = np.array(accel_ts)
        vehicle.x = np.array(position_ts)
        return vehicle

    def timeEvolveEgo(self,
                      leader,
                      ):
        #set initial conditions
        vehicle = oem()
        self.setPars()
        speed_ts = []
        accel_ts = []
        position_ts = []
        speed_ts.append(self.varDict['curr_veh_velocity'])
        accel_ts.append(0)
        position_ts.append(self.veh_position)
        for i in range(self.time.shape[0]):
            #Set time and leader stuff
            self.varDict['curr_timestep'] = self.time[i]
            self.varDict['curr_lead_veh_acceleration'] = leader.a[i]
            self.lead_speed = leader.v[i]
            self.lead_position = leader.x[i]
            #call OL
            self.call()
            #Set follower
            self.veh_position = (
                + self.veh_position
                + self.varDict['curr_veh_velocity'] * self.varDict['curr_ts_length']
                + .5 * self.veh_autonomous_operational_acceleration.value * self.varDict['curr_ts_length']**2
                )
            self.varDict['curr_veh_velocity'] = (
                + self.varDict['curr_veh_velocity']
                + self.veh_autonomous_operational_acceleration.value * self.varDict['curr_ts_length']
                )
            self.varDict['curr_lead_veh_rel_velocity'] = self.varDict['curr_veh_velocity'] - self.lead_speed
            self.varDict['curr_veh_setspeed'] = self.veh_cc_setpoint.value

            self.varDict['prev_veh_cc_setpoint'] = self.veh_cc_setpoint.value

            self.varDict['curr_veh_used_distance_headway'] = self.lead_position - self.veh_position - self.veh_length
            self.varDict['prev_veh_distance_headway'] = self.lead_position - self.veh_position - self.veh_length
            self.varDict['prev_veh_cruisecontrol_acceleration'] = self.veh_cruisecontrol_acceleration.value
            self.varDict['prev_veh_executed_acceleration'] = self.veh_autonomous_operational_acceleration.value

            speed_ts.append(self.varDict['curr_veh_velocity'])
            accel_ts.append(self.veh_autonomous_operational_acceleration.value)
            position_ts.append(self.veh_position)
        vehicle.v = np.array(speed_ts)
        vehicle.a = np.array(accel_ts)
        vehicle.x = np.array(position_ts)
        return vehicle

    def printOutput(self,):
        # Print the return values
        if self.success.value > 0:
            print(self.veh_autonomous_operational_acceleration.value)
            print(self.veh_autonomous_operational_mixingmode.value)
            print(self.veh_autonomous_operational_warning.value)
            print(self.veh_cc_setpoint.value)
            print(self.veh_cruisecontrol_acceleration.value)
        else:
            print('An error occurred while calling DLL')

    def call(self,):
        curr_lead_veh_acceleration = ctypes.c_double(self.varDict['curr_lead_veh_acceleration'])
        curr_lead_veh_id = ctypes.c_long(self.varDict['curr_lead_veh_id'])
        curr_lead_veh_rel_velocity = ctypes.c_double(self.varDict['curr_lead_veh_rel_velocity'])
        curr_lead_veh_type = ctypes.c_long(self.varDict['curr_lead_veh_type'])
        curr_timestep = ctypes.c_double(self.varDict['curr_timestep'])
        curr_ts_length = ctypes.c_double(self.varDict['curr_ts_length'])
        curr_veh_id = ctypes.c_long(self.varDict['curr_veh_id'])
        curr_veh_setspeed = ctypes.c_double(self.varDict['curr_veh_setspeed'])
        curr_veh_type = ctypes.c_long(self.varDict['curr_veh_type'])
        curr_veh_controller_in_use = ctypes.c_long(self.varDict['curr_veh_controller_in_use'])
        curr_veh_ACC_h = ctypes.c_double(self.varDict['curr_veh_ACC_h'])
        curr_veh_CACC_h= ctypes.c_double(self.varDict['curr_veh_CACC_h'])
        curr_veh_used_distance_headway = ctypes.c_double(self.varDict['curr_veh_used_distance_headway'])
        curr_veh_used_rel_vel = ctypes.c_double(self.varDict['curr_veh_used_rel_vel'])
        curr_veh_velocity = ctypes.c_double(self.varDict['curr_veh_velocity'])
        curr_veh_autonomous_operational_warning = ctypes.c_long(self.varDict['curr_veh_autonomous_operational_warning'])
        curr_veh_platooning_max_acceleration = ctypes.c_double(self.varDict['curr_veh_platooning_max_acceleration'])

        prev_veh_cc_setpoint = ctypes.c_double(self.varDict['prev_veh_cc_setpoint'])
        prev_veh_cruisecontrol_acceleration = ctypes.c_double(self.varDict['prev_veh_cruisecontrol_acceleration'])
        prev_veh_distance_headway = ctypes.c_double(self.varDict['prev_veh_distance_headway'])
        prev_veh_executed_acceleration = ctypes.c_double(self.varDict['prev_veh_executed_acceleration'])

        # Define variables for return values: These are placeholders, no action required
        self.veh_autonomous_operational_acceleration = ctypes.c_double(1)
        self.veh_autonomous_operational_mixingmode = ctypes.c_long(1)
        self.veh_autonomous_operational_warning = ctypes.c_double(1)
        self.veh_cc_setpoint = ctypes.c_double(1)
        self.veh_cruisecontrol_acceleration = ctypes.c_double(1)
        self.success = ctypes.c_int(0)

        self.lib.operational_controller(
        curr_lead_veh_acceleration,
        curr_lead_veh_id,
        curr_lead_veh_rel_velocity,
        curr_lead_veh_type,
        curr_timestep,
        curr_ts_length,
        curr_veh_id,
        curr_veh_setspeed,
        curr_veh_type,
        curr_veh_controller_in_use,
        curr_veh_ACC_h,
        curr_veh_CACC_h,
        curr_veh_used_distance_headway,
        curr_veh_used_rel_vel,
        curr_veh_velocity,
        curr_veh_autonomous_operational_warning,
        curr_veh_platooning_max_acceleration,
        prev_veh_cc_setpoint,
        prev_veh_cruisecontrol_acceleration,
        prev_veh_distance_headway,
        prev_veh_executed_acceleration,
        ctypes.byref(self.veh_autonomous_operational_acceleration),
        ctypes.byref(self.veh_autonomous_operational_mixingmode),
        ctypes.byref(self.veh_autonomous_operational_warning),
        ctypes.byref(self.veh_cc_setpoint),
        ctypes.byref(self.veh_cruisecontrol_acceleration),
        ctypes.byref(self.success))

    def  runFullScenario(self,):
        self.sPars['extraGap'] = 30
        self.sPars['lead_position'] = 800
        self.setMetaPars()
        l = self.defineLeaderProfile(scenario = 'cut-in')
        self.sPars['lead_position'] = 800 + 25
        v4 = self.timeEvolveEgo(leader = l)
        for i in range(0,self.testDurationInSeconds):
            if i < 500:
                v4.x[i] = l.x[i];
        self.sPars['extraGap'] = 0
        self.sPars['lead_position'] = 800
        self.sPars['lead_position'] = v4.x[0]
        v = self.timeEvolveEgo(v4)
        self.sPars['lead_position'] = v.x[0]
        v2 = self.timeEvolveEgo(v)
        self.sPars['lead_position'] = v2.x[0]
        v3 = self.timeEvolveEgo(v2)
        self.sPars['lead_position'] = v3.x[0]
        fleet = []
        fleet.append(l)
        fleet.append(v)
        fleet.append(v2)
        fleet.append(v3)
        fleet.append(v4)
        return fleet

def main():
    olt = operationalLayerTest()
    olt.runFullScenario()
    # olt.setPars()
    #olt.run()
    # v = olt.defineLeaderProfile()
    # v1 = olt.timeEvolveEgo(leader = v)


if __name__ == '__main__':
    main()