from ensemble.component.vehicles import Vehicle
from ensemble.tools.constants import DCT_PLT_CONST
class PlatoonVehicle(Vehicle):
    """ This class is to store functionality of a platoon vehicle"""
    def __init__(self,ego_position=1,
                 platoon_length=1,
                 desired_platoon_speed=20,
                 maximum_speed=25,
                maximum_acceleration=2.0, 
                maximum_deceleration=-2.0 ,
                 state="STANDALONE",
                 intruder=False,
                 split_request=False):
        self.ego_position=ego_position
        self.platoon_length=platoon_length
        self. desired_platoon_speed=desired_platoon_speed
        self.maximum_speed=maximum_speed
        self.maximum_acceleration=maximum_acceleration
        self.intruder=intruder
        self.split_request=split_request
        self.state=state
    
    def joinable(self):
        if (self.leader.ego_position() <DCT_PLT_CONST['max_platoon_length']) and \
            (self.gap_distance_error()<DCT_PLT_CONST['max_connection_distance']) :
            return True
        else:
            return False
    def relative_speed(self):
        speed_diff=self.speed-self.leader.speed
        return speed_diff
    def gap_distance_error(self):
        gap=self.leader.posX - self.posX-self.leader.length
        return gap
    def distance_to_leader(self):
        dist=self.leader.posX - self.posX

    def join_request(self):
        if   (self.leader.joinable() == True):
            return True
        else:
            return False

    def cancel_join_request(self):  # add lane change and other conditions
        if  (self.leader.is_platoon_vehicle() == False):
            return True
        else:
            return False

    def confirm_platoon(self):
        if  (self.relative_speed() < DCT_PLT_CONST['max_platoon_length']) \
                and (self.gap_distance_error() < DCT_PLT_CONST['max_gap_distance_error']):
            self.state = "PLATOON"
            self.ego_position = self.leader.ego_position + 1  # update position

    def platoon_split(self):
        if  ((self.leader.is_platoon_vehicle() == False)) or \
                (self.split_request() == True) or (self.leader.split_request() == True):
            return True

    def rejoin_platoon(self):
        if  (self.split_request() == False) and \
                (self.distance_to_leader < DCT_PLT_CONST['standalone_gap']) and (
                self.leader.is_platoon_vehicle() == False):
            return True
        else:
            return False

    def leave_platoon(self, platoonvehicle):
        if (platoonvehicle.distance_to_leader > DCT_PLT_CONST['standalone_gap']):
            return True
        else:
            return False

