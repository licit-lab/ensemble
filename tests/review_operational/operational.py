# from ensemble.component.vehicles import Vehicle

from dataclasses import dataclass, field
import pandas as pd
from ctypes import c_double, cdll, c_long, c_int, CDLL, byref


cdll_path = "/Users/andresladino/Documents/01-Code/02-Python/mypkgs/ensemble/ensemble/libs/darwin/OperationalDLL.dylib"
cacc = cdll.LoadLibrary(cdll_path)


@dataclass
class CACC:
    # Leader info
    curr_lead_veh_acceleration: c_double = field(default=c_double(0))
    curr_lead_veh_id: c_long = field(default=c_long(0))
    curr_lead_veh_rel_velocity: c_double = field(default=c_double(0))
    curr_lead_veh_type: c_long = field(default=c_long(0))

    # Current time info
    curr_timestep: c_double = field(default=c_double(0))
    curr_ts_length: c_double = field(default=c_double(0))
    curr_veh_id: c_long = field(default=c_long(0))
    curr_veh_setspeed: c_double = field(default=c_double(0))
    curr_veh_type: c_long = field(default=c_long(1))

    # ? Codes 1,2, ,1-ACC ,2-CACC
    curr_veh_controller_in_use: c_long = field(default=c_long(2))

    # Reference headways
    curr_veh_ACC_h: c_double = field(default=c_double(0))
    curr_veh_CACC_h: c_double = field(default=c_double(0))

    # Ego headway space
    curr_veh_used_distance_headway: c_double = field(default=c_double(0))

    # Ego vehicle Dv,v
    curr_veh_used_rel_vel: c_double = field(default=c_double(0))
    curr_veh_velocity: c_double = field(default=c_double(0))

    # ? Codes ?
    curr_veh_autonomous_operational_warning: c_long = field(default=c_long(0))

    # Positive value - symmetric
    curr_veh_platooning_max_acceleration: c_double = field(
        default=c_double(2.0)
    )

    # Past time info
    prev_veh_cc_setpoint: c_double = field(default=c_double(0))
    # Check placeholdeers -> veh_cruisecontrol_acceleration
    prev_veh_cruisecontrol_acceleration: c_double = field(default=c_double(0))
    prev_veh_distance_headway: c_double = field(default=c_double(0))
    # a
    prev_veh_executed_acceleration: c_double = field(default=c_double(0))

    # Placeholders
    veh_autonomous_operational_acceleration: c_double = field(
        default=c_double(1)
    )
    veh_autonomous_operational_mixingmode: c_long = field(default=c_long(1))
    veh_autonomous_operational_warning: c_double = field(default=c_double(1))
    veh_cc_setpoint: c_double = field(default=c_double(1))
    veh_cruisecontrol_acceleration: c_double = field(default=c_double(1))
    success: c_int = field(default=c_int(0))

    lib: CDLL = field(default=cacc)

    def _apply_control(self):
        self.lib.operational_controller(
            self.curr_lead_veh_acceleration,
            self.curr_lead_veh_id,
            self.curr_lead_veh_rel_velocity,
            self.curr_lead_veh_type,
            self.curr_timestep,
            self.curr_ts_length,
            self.curr_veh_id,
            self.curr_veh_setspeed,
            self.curr_veh_type,
            self.curr_veh_controller_in_use,
            self.curr_veh_ACC_h,
            self.curr_veh_CACC_h,
            self.curr_veh_used_distance_headway,
            self.curr_veh_used_rel_vel,
            self.curr_veh_velocity,
            self.curr_veh_autonomous_operational_warning,
            self.curr_veh_platooning_max_acceleration,
            self.prev_veh_cc_setpoint,
            self.prev_veh_cruisecontrol_acceleration,
            self.prev_veh_distance_headway,
            self.prev_veh_executed_acceleration,
            byref(self.veh_autonomous_operational_acceleration),
            byref(self.veh_autonomous_operational_mixingmode),
            byref(self.veh_autonomous_operational_warning),
            byref(self.veh_cc_setpoint),
            byref(self.veh_cruisecontrol_acceleration),
            byref(self.success),
        )
        return (
            self.veh_autonomous_operational_acceleration.value,
            self.veh_cruisecontrol_acceleration.value,
        )

    def __call__(self, leader, ego, r1, t, T):
        """ Asumes 0 index for lead 1 for follower
            
            a: real acceleration
            x: postition
            v: speed
            s: spacing 
            u: control 

            D: delta
            P: past

            Args:
                leader(dict): vehicle 0 keys, a,x,v,Dv,Pu,Ps
                ego(dict): vehicle 1, keys, a,x,v,Dv,Pu,Ps
                r1(dict): reference 1 keys, v,vp  
                t(float): time stamp
                T(float): sampling time
        """
        self.curr_lead_veh_acceleration = c_double(leader["a"])
        self.curr_lead_veh_id = c_long(leader["id"])
        self.curr_lead_veh_rel_velocity = c_double(leader["Dv"])
        # self.curr_lead_veh_type=c_long(0)
        self.curr_timestep = c_double(t)
        # self.curr_ts_length = c_double(T)
        self.curr_veh_id = c_long(ego["id"])
        self.curr_veh_setspeed = c_double(r1["v"])
        # self.curr_veh_type=c_long(1)
        # self.curr_veh_controller_in_use=c_long(2)
        self.curr_veh_ACC_h = c_double(r1["s"])
        self.curr_veh_CACC_h = c_double(r1["s"])
        self.curr_veh_used_distance_headway = c_double(leader["x"] - ego["x"])
        self.curr_veh_used_rel_vel = c_double(leader["v"] - ego["v"])
        self.curr_veh_velocity = c_double(ego["v"])
        # self.curr_veh_autonomous_operational_warning
        # self.curr_veh_platooning_max_acceleration
        self.prev_veh_cc_setpoint = c_double(r1["Pv"])
        self.prev_veh_cruisecontrol_acceleration = c_double(ego["Pint"])
        self.prev_veh_distance_headway = c_double(ego["Ps"])
        self.prev_veh_executed_acceleration = c_double(ego["Pu"])
        return self._apply_control()

    def update_value(self, **kwargs):
        """Update values to compute control"""
        for key, value in kwargs.items():
            setattr(self, key, value)


if __name__ == "__main__":
    c = CACC()
    r = array() # vector
    for reference in r:
        
        c(leader_veh,follower_vehicle,reference, time_step, time_sampling)
