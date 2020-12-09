import os
import sys
import ctypes
import platform
if platform.system() == 'Windows':
	print('Running on win')
	file_dll = './OperationalDLL.dll'
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
curr_lead_veh_acceleration = ctypes.c_double(2.0)
curr_lead_veh_id = ctypes.c_long(40)
curr_lead_veh_rel_velocity = ctypes.c_double(-1.0)
curr_lead_veh_type = ctypes.c_long(10)
curr_timestep = ctypes.c_double(55.0)
curr_ts_length = ctypes.c_double(0.1)
curr_veh_id = ctypes.c_long(10)
curr_veh_setspeed = ctypes.c_double(88/3.6)
curr_veh_type = ctypes.c_long(10)
curr_veh_controller_in_use = ctypes.c_long(10)
curr_veh_ACC_h = ctypes.c_double(1.6)
curr_veh_CACC_h= ctypes.c_double(0.6)
curr_veh_used_distance_headway = ctypes.c_double(20.0)
curr_veh_used_rel_vel = ctypes.c_double(-1.0)
curr_veh_velocity = ctypes.c_double(85./3.6)
curr_veh_autonomous_operational_warning = ctypes.c_long(10)
curr_veh_platooning_max_acceleration = ctypes.c_double(2.0)

prev_veh_cc_setpoint = ctypes.c_double(85./3.6)
prev_veh_cruisecontrol_acceleration = ctypes.c_double(2.0)
prev_veh_distance_headway = ctypes.c_double(20.0)
prev_veh_executed_acceleration = ctypes.c_double(-2.0)


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
	print(veh_autonomous_operational_acceleration.value)
	print(veh_autonomous_operational_mixingmode.value)
	print(veh_autonomous_operational_warning.value)
	print(veh_cc_setpoint.value)
	print(veh_cruisecontrol_acceleration.value)
else:
	print('An error occurred while calling DLL')
