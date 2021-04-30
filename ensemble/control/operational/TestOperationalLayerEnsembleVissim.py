import os
import sys
import ctypes
import platform
import os
import numpy as np
from random import gauss
import win32com.client as com
def get_acceleration(lead_veh_acceleration,lead_veh_id,lead_veh_rel_velocity,lead_veh_type,timestep,
                     veh_id,veh_setspeed,veh_type,veh_used_distance_headway,veh_used_rel_vel,veh_velocity,
                     veh_distance_headway,prev_veh_executed_acceleration,
                                       prev_veh_cc_setpoint,prev_veh_cruisecontrol_acceleration):
    if platform.system() == 'Windows':
        print('Running on win')
        filepath = "L:\\UserData\\Kingsley\\PythonEnsembleTestBed"

        file_dll = os.path.join(filepath, 'OperationalDLL.dll')
        #file_dll = './OperationalDLL.dll'
    elif platform.system() == 'Darwin':
        print('Running on mac')
        file_dll = 'OperationalDLL.dylib'
    else:
        print('System not supported')
        sys.exit()

    # Load operational DLL
    lib = None
    try:
        lib = ctypes.cdll.LoadLibrary(file_dll)
    except:
        print('Error: DLL file could not be found')
        quit()

    # Set input values: Write value's for current vehicle, in current timestep
    curr_lead_veh_acceleration = ctypes.c_double(lead_veh_acceleration) #2.0
    curr_lead_veh_id = ctypes.c_long(lead_veh_id) #40
    curr_lead_veh_rel_velocity = ctypes.c_double(lead_veh_rel_velocity ) #-1.0
    curr_lead_veh_type = ctypes.c_long(lead_veh_type) #10
    curr_timestep = ctypes.c_double(timestep) #55.0
    curr_ts_length = ctypes.c_double(0.1)
    curr_veh_id = ctypes.c_long(veh_id) #10
    curr_veh_setspeed = ctypes.c_double(veh_setspeed) #88/3.6
    curr_veh_type = ctypes.c_long(veh_type) #10
    curr_veh_controller_in_use = ctypes.c_long(1) # from tactical layer 1=ACC,2=CACC
    curr_veh_ACC_h = ctypes.c_double(1.6)
    curr_veh_CACC_h = ctypes.c_double(0.6)
    curr_veh_used_distance_headway = ctypes.c_double(veh_used_distance_headway)#20.0
    curr_veh_used_rel_vel = ctypes.c_double(veh_used_rel_vel) #-1.0
    curr_veh_velocity = ctypes.c_double(veh_velocity) #85/3.6
    curr_veh_autonomous_operational_warning = ctypes.c_long(10)
    curr_veh_platooning_max_acceleration = ctypes.c_double(2.0)

    prev_veh_cc_setpoint = ctypes.c_double(prev_veh_cc_setpoint)
    prev_veh_cruisecontrol_acceleration = ctypes.c_double(prev_veh_cruisecontrol_acceleration)
    prev_veh_distance_headway = ctypes.c_double(veh_distance_headway) #20.0
    prev_veh_executed_acceleration = ctypes.c_double(prev_veh_executed_acceleration) #-2.0

    # Define variables for return values: These are placeholders, no action required
    veh_autonomous_operational_acceleration = ctypes.c_double(1)
    veh_autonomous_operational_mixingmode = ctypes.c_long(1)
    veh_autonomous_operational_warning = ctypes.c_double(1)
    veh_cc_setpoint = ctypes.c_double(1)
    veh_cruisecontrol_acceleration = ctypes.c_double(1)
    success = ctypes.c_int(0)

    print("Now call the OL itself...")

    # Call operational controller
    lib.operational_controller(
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
        ctypes.byref(veh_autonomous_operational_acceleration),
        ctypes.byref(veh_autonomous_operational_mixingmode),
        ctypes.byref(veh_autonomous_operational_warning),
        ctypes.byref(veh_cc_setpoint),
        ctypes.byref(veh_cruisecontrol_acceleration),
        ctypes.byref(success))

    # Print the return values
    if success.value > 0:
        veh_acceleration=veh_autonomous_operational_acceleration.value
        #print(veh_autonomous_operational_mixingmode.value)
        #print(veh_autonomous_operational_warning.value)
        veh_cc_set_point=veh_cc_setpoint.value
        veh_cruise_control_acceleration=veh_cruisecontrol_acceleration.value
    else:
        veh_acceleration=-999
        veh_cc_setpoint=-999
        veh_cruise_control_acceleration=-999
        print('An error occurred while calling DLL')
    return veh_acceleration,veh_cc_setpoint,veh_cruise_control_acceleration


Vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
GlosaNetworkPath='D:\\Projects\\ENSEMBLE\\Vissim_networks\\Pipeline'#'L:\\UserData\\Kingsley\\Ensemble'
    #'L:\\UserData\\Kingsley\\SafeDriving'
    #'L:\\UserData\\Kingsley\\Ensemble'#'C:\\Users\\Public\\Documents\\GLOSA\\GlosaTrafficLight'
Filename= os.path.join(GlosaNetworkPath, 'Pipeline.inpx')
#os.path.join(GlosaNetworkPath, 'KnooppuntZonzeelBackup.inpx') #os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.inpx')
#os.path.join(GlosaNetworkPath, 'TestNetwork.inpx')
flag_read_additionally  = False # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
Vissim.LoadNet(Filename, flag_read_additionally)
## Load a Layout:
Filename = os.path.join(GlosaNetworkPath, 'Pipeline.layx')
#os.path.join(GlosaNetworkPath, 'KnooppuntZonzeelBackup.layx')
    #os.path.join(GlosaNetworkPath, 'TestNetwork.layx')
    #os.path.join(GlosaNetworkPath, 'KnooppuntZonzeelBackup.layx')#os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.layx')
Vissim.LoadLayout(Filename)

End_of_simulation = 6000 # simulation second [s]
Simulation_Resolution = 10 # simulation second [s]
Number_Runs=4
Simulation_Period=300
Vissim.Simulation.SetAttValue('SimRes', Simulation_Resolution)
Vissim.Simulation.SetAttValue('NumRuns', Number_Runs)
Vissim.Simulation.SetAttValue('SimPeriod', Simulation_Period)
#UDA6
#Vissim.Net.UserDefinedAttributes.AddUserDefinedDataAttribute(6,'Vehicle','vehAcceleration','vehAcceleration',2,0)
#Vissim.Net.UserDefinedAttributes.ItemByKey(6).SetAttValue('DefValue',-1)
#UDA6
Vissim.Net.UserDefinedAttributes.AddUserDefinedDataAttribute(3,'Vehicle','COM_cruise_control_Ac','COM_cruise_control_Ac',2,0)
Vissim.Net.UserDefinedAttributes.ItemByKey(3).SetAttValue('DefValue',-1)

#UDA
Vissim.Net.UserDefinedAttributes.AddUserDefinedDataAttribute(4,'Vehicle','COM_cc_setpoint','COM_cc_setpoint',2,0)
Vissim.Net.UserDefinedAttributes.ItemByKey(4).SetAttValue('DefValue',-1)
def get_leader_info(Vehicle):
    lead_veh_id = Vehicle.AttValue('LeadTargNo')
    lead_veh_type = Vehicle.AttValue('LeadTargType')
    if lead_veh_type == 'VEHICLE' and lead_veh_id != None:
        try:
            front_vehicle = Vissim.Net.Vehicles.ItemByKey(lead_veh_id)
        except:
            front_vehicle = -1
    else:
        front_vehicle=-1
    return front_vehicle
#prev_veh_cc_setpoint = np.zeros(number_of_vehicles)
for i in range(6000):
    for Vehicle in Vissim.Net.Vehicles.FilteredBy("[VEHTYPE\\NO]=210"):
        lead_veh=get_leader_info(Vehicle)
        if lead_veh!=-1 and (Vehicle.AttValue('Lane')==lead_veh.AttValue('Lane')):
            #simulation info
            timestep=Vehicle.AttValue('SimSec')
            #Ego Info
            print((Vehicle.AttValue('Lane')))
            veh_id=Vehicle.AttValue('No')
            veh_setspeed=Vehicle.AttValue('DesSpeed')/3.6
            veh_type=Vehicle.AttValue('VehType\\No')
            veh_used_distance_headway=Vehicle.AttValue('FollowDistNet')
            veh_used_rel_vel=(Vehicle.AttValue('Speed')-lead_veh.AttValue('Speed'))/3.6
            veh_velocity=Vehicle.AttValue('Speed')/3.6
            veh_distance_headway=Vehicle.AttValue('FollowDistNet')
            prev_veh_executed_acceleration = Vehicle.AttValue('COM_Ac')
            prev_veh_cc_setpoint = Vehicle.AttValue('COM_cc_setpoint')
            prev_veh_cruisecontrol_acceleration=Vehicle.AttValue('COM_cruise_control_Ac')
            #veh_executed_acceleration=a_prev[veh_id]
            #veh_cc_setpoint=prev_veh_cc_setpoint[veh_id]
            # Leader Info
            lead_veh_acceleration=lead_veh.AttValue('Acceleration')
            lead_veh_id=lead_veh.AttValue('No')
            lead_veh_rel_velocity=(Vehicle.AttValue('Speed')-lead_veh.AttValue('Speed'))/3.6
            lead_veh_type=lead_veh.AttValue('VehType\\No')

            curr_veh_executed_acceleration,curr_veh_cc_set_point,curr_veh_cruisecontrol_acceleration=get_acceleration(lead_veh_acceleration,lead_veh_id,lead_veh_rel_velocity,lead_veh_type,timestep,
                     veh_id,veh_setspeed,veh_type,veh_used_distance_headway,veh_used_rel_vel,veh_velocity,
                     veh_distance_headway,prev_veh_executed_acceleration,
                                       prev_veh_cc_setpoint,prev_veh_cruisecontrol_acceleration)
            # a=call vehicle_model(curr_veh_executed_acceleration)
            write_file('file_variables.txt')
            Vehicle.SetAttValue('COM_Ac',curr_veh_executed_acceleration)
            #Vehicle.SetAttValue('COM_Ac', a)
            Vehicle.SetAttValue('COM_At',3)
            Vehicle.SetAttValue('COM_cc_setpoint', curr_veh_cc_set_point)
            Vehicle.SetAttValue('COM_cruise_control_Ac', curr_veh_cruisecontrol_acceleration)

        else:
            continue
    Vissim.Simulation.RunSingleStep()
