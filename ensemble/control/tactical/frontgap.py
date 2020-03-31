""" 
    This module will implement functionalities associated with the front gap handling

"""

from ensemble.state.platoon import StandAlone, Platoon, Join, Split, CutIn, CutThrough


class FrontGapCoord(object):
    """ This class models front gap coordination maneuvers for a single vehicle 
    """

    def __init__(self, vehicle):
        """ Initial condition of a front gap coordinator
        """
        self.state = StandAlone()

    def request_info_front_target(self, vehicle):
        if vehicle.leader.joinable():
            self.state = self.state.switchto("join")

    def confirm_platoon(self, vehicle):
        if vehicle.speed == 90 and vehicle.deltaspeed < 5:
            self.state = self.state.switchto("platoon")
