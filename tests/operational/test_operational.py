"""
    Unit testing for ensemble.control.operational
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import sys
from ctypes import cdll, c_int, c_double, c_float, c_long, byref
import platform
import pytest
from unittest.case import TestCase

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble import configurator
from ensemble.tools.constants import DEFAULT_CACC_PATH
from ensemble.control.operational import CACC
import platform

# ============================================================================
# TESTS
# ============================================================================


@pytest.fixture
def controller_libpath():
    return DEFAULT_CACC_PATH


@pytest.mark.skipif(platform.system() == "Linux", reason="Not .so available")
def test_load_dll(controller_libpath):
    handle = cdll.LoadLibrary(controller_libpath)
    assert handle._name == controller_libpath


@pytest.mark.skipif(platform.system() == "Linux", reason="Not .so available")
def test_specific_output(controller_libpath):
    controller = cdll.LoadLibrary(controller_libpath)
    # Set input values: Write value's for current vehicle, in current timestep

    # Leader info
    curr_lead_veh_acceleration = c_double(2.0)
    curr_lead_veh_id = c_long(0)
    curr_lead_veh_rel_velocity = c_double(-1.0)
    curr_lead_veh_type = c_long(1)

    # Current time info
    curr_timestep = c_double(55.0)
    curr_ts_length = c_double(0.1)

    ## Ego info
    curr_veh_id = c_long(1)
    curr_veh_type = c_long(1)

    # Speed setpoint
    curr_veh_setspeed = c_double(88 / 3.6)

    # Control under use: 1-ACC ,2-CACC
    curr_veh_controller_in_use = c_long(2)

    # Setpoint timegap headways
    curr_veh_ACC_h = c_double(1.6)
    curr_veh_CACC_h = c_double(0.6)

    # Ego headway space
    curr_veh_used_distance_headway = c_double(20.0)

    # Ego vehicle Dv,v
    curr_veh_used_rel_vel = c_double(-1.0)
    curr_veh_velocity = c_double(85.0 / 3.6)

    # Unclear
    curr_veh_autonomous_operational_warning = c_long(10)

    # Max accel/deccel  - Positive value - symmetric
    curr_veh_platooning_max_acceleration = c_double(2.0)

    # Past time info
    # Speed setpoint -> curr_veh_setspeed
    prev_veh_cc_setpoint = c_double(85.0 / 3.6)
    # Return values -> veh_cruisecontrol_acceleration
    prev_veh_cruisecontrol_acceleration = c_double(2.0)
    # Ego headway space → curr_veh_used_distance_headway
    prev_veh_distance_headway = c_double(20.0)
    # Return values → veh_autonomous_operational_acceleration
    prev_veh_executed_acceleration = c_double(-2.0)

    # Return values: These are placeholders, no action required
    veh_autonomous_operational_acceleration = c_double(1)
    veh_autonomous_operational_mixingmode = c_long(1)
    veh_autonomous_operational_warning = c_double(1)
    veh_cc_setpoint = c_double(1)
    veh_cruisecontrol_acceleration = c_double(2.0)
    success = c_int(0)

    controller.operational_controller(
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

    assert success.value > 0
    assert veh_autonomous_operational_acceleration.value == -1.0318114116459798
    assert veh_autonomous_operational_mixingmode.value == 2
    assert veh_autonomous_operational_warning.value == 10.0
    assert veh_cc_setpoint.value == 24.444444444444443
    assert veh_cruisecontrol_acceleration.value == 0.0


@pytest.mark.skipif(platform.system() == "Linux", reason="Not .so available")
def test_cacc_artifact(controller_libpath):
    control = CACC()
    control.lib._name == controller_libpath


@pytest.mark.skipif(platform.system() == "Linux", reason="Not .so available")
def test_cacc_call_data_null():
    control = CACC()
    leader = {
        "id": 0,
        "a": 2.0,
        "x": 50,
        "v": 85 / 3.6,
        "s": 0,
        "u": 0,
        "Dv": -1,
        "Pu": 0,
        "Ps": 0,
    }
    ego = {
        "id": 1,
        "a": 0,
        "x": 30,
        "v": 85 / 3.6,
        "s": 0,
        "u": 0,
        "Dv": 0,
        "Pu": 0,
        "Ps": 0,
        "Pint": 0,
    }
    ref = {
        "g_acc": 0.6,
        "g_cacc": 1.6,
        "v": 88 / 3.6,
        "Pv": 0,
    }
    control(leader, ego, ref, 0, 1 / 10)

    assert control.success.value > 0
    assert control.veh_autonomous_operational_acceleration.value < 0
