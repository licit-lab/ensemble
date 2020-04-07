""" 
    This module will implement functionalities associated with the front gap handling

"""

from ensemble.state.platoon import StandAlone, Platoon, Join, Split


class FrontGapCoord(object):
    """ This class models front gap coordination maneuvers for a single platoonvehicle 
    """

    def __init__(self, platoonvehicle):
        """ Initial condition of a front gap coordinator
        """
        self.state = StandAlone()


    def join_request(self, platoonvehicle):
        if self.state==StandAlone()and  (platoonvehicle.leader.joinable()==True)  :
            self.state = self.state.switchto("join")
    def cancel_join_request(self,platoonvehicle):
        if (self.state==Join()) and  (platoonvehicle.leader.is_platoon_vehicle== False):
            self.state = self.state.switchto("standalone")


    def confirm_platoon(self, platoonvehicle):
        if (self.state==Join()) and  (platoonvehicle.relative_speed() < max_relative_speed) \
                and (platoonvehicle.gap_distance_error() < max_gap_distance_error):
            self.state = self.state.switchto("platoon")
            platoonvehicle.ego_position = platoonvehicle.leader.ego_position + 1 # update position
    def platoon_split(self,platoonvehicle):
        if( (self.state==Platoon()) and  (platoonvehicle.leader.is_platoon_vehicle()==False )) or \
        (platoonvehicle.split_request() == True) :
            self.state=self.state.switchto("split")


    def rejoin_platoon(self,platoonvehicle):
        if (self.state==Split() )and  (platoonvehicle.split_request() == False) and \
                     (platoonvehicle.distance_to_leader<stand_alone_gap):
            self.state = self.state.switchto("platoon")
    def leave_platoon(self,platoonvehicle):
        if (self.state==Split())  and ( platoonvehicle.distance_to_leader > stand_alone_gap):
            self.state = self.state.switchto("standalone")
    
           



        