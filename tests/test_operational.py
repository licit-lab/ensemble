"""
    Test suite for the shared library containing the operational layer.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import sys
from ctypes import cdll, c_int, c_double, c_float, c_long, byref
import platform
import unittest
from unittest.case import TestCase

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble import configurator

# ============================================================================
# TESTS
# ============================================================================


class TestLoadLibrary(unittest.TestCase):
    def setUp(self):
        opsys = platform.system().lower()
        if opsys == "windows":
            self.path_dll = os.path.join(os.getcwd(), "ensemble", "libs", opsys, "OperationalDLL.dll")
        elif opsys == "darwin":
            self.path_dll = os.path.join(os.getcwd(), "ensemble", "libs", opsys, "OperationalDLL.dylib")
        else:
            print("System not supported")
            sys.exit()

    def test_load_dll(self):
        handle = cdll.LoadLibrary(self.path_dll)
        self.assertEqual(handle._name, self.path_dll)


class TestQueryOperationalDLL(unittest.TestCase):
    def setUp(self):
        opsys = platform.system().lower()
        if opsys == "windows":
            self.path_dll = os.path.join(os.getcwd(), "ensemble", "libs", opsys, "OperationalDLL.dll")
        elif opsys == "darwin":
            self.path_dll = os.path.join(os.getcwd(), "ensemble", "libs", opsys, "OperationalDLL.dylib")
        else:
            print("System not supported")
            sys.exit()
        self.handle = cdll.LoadLibrary(self.path_dll)

    def test_specific_output(self):
        # Set input values: Write value's for current vehicle, in current timestep
        curr_lead_veh_acceleration = c_double(2.0)
        curr_lead_veh_id = c_long(40)
        curr_lead_veh_rel_velocity = c_double(-1.0)
        curr_lead_veh_type = c_long(10)
        curr_timestep = c_double(55.0)
        curr_ts_length = c_double(0.1)
        curr_veh_id = c_long(10)
        curr_veh_setspeed = c_double(88 / 3.6)
        curr_veh_type = c_long(10)
        curr_veh_controller_in_use = c_long(10)
        curr_veh_ACC_h = c_double(1.6)
        curr_veh_CACC_h = c_double(0.6)
        curr_veh_used_distance_headway = c_double(20.0)
        curr_veh_used_rel_vel = c_double(-1.0)
        curr_veh_velocity = c_double(85.0 / 3.6)
        curr_veh_autonomous_operational_warning = c_long(10)
        curr_veh_platooning_max_acceleration = c_double(2.0)

        prev_veh_cc_setpoint = c_double(85.0 / 3.6)
        prev_veh_cruisecontrol_acceleration = c_double(2.0)
        prev_veh_distance_headway = c_double(20.0)
        prev_veh_executed_acceleration = c_double(-2.0)

        # Define variables for return values: These are placeholders, no action required
        veh_autonomous_operational_acceleration = c_double(1)
        veh_autonomous_operational_mixingmode = c_long(1)
        veh_autonomous_operational_warning = c_double(1)
        veh_cc_setpoint = c_double(1)
        veh_cruisecontrol_acceleration = c_double(1)
        success = c_int(0)

        self.handle.operational_controller(
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
            byref(veh_autonomous_operational_acceleration),
            byref(veh_autonomous_operational_mixingmode),
            byref(veh_autonomous_operational_warning),
            byref(veh_cc_setpoint),
            byref(veh_cruisecontrol_acceleration),
            byref(success),
        )

        self.assertGreater(success.value, 0)

        self.assertEqual(veh_autonomous_operational_acceleration.value, -1.0318114116459798)
        self.assertEqual(veh_autonomous_operational_mixingmode.value, 2)
        self.assertEqual(veh_autonomous_operational_warning.value, 10.0)
        self.assertEqual(veh_cc_setpoint.value, 24.444444444444443)
        self.assertEqual(veh_cruisecontrol_acceleration.value, 0.0)
