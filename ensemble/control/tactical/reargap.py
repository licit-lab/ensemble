from ensemble.state.platoon import StandAlone, Platoon, Join, Split
from .frontgap import FrontGapCoord


class RearGapCoord(object):
    """This class models rear gap coordination maneuvers for a single platoonvehicle"""

    def __init__(self, platoonvehicle):
        """Initial condition of a front gap coordinator"""
        follower = platoonvehicle.follower()
        self.follower_frontgapcoord = FrontGapCoord(follower)
        self.state = StandAlone()

    def standalone_mode(self, platoonvehicle):
        if self.follower_frontgapcoord.state == StandAlone():
            self.state = self.state.switchto("standalone")

    def join_mode(self, platoonvehicle):
        if self.state == StandAlone() and self.follower_frontgapcoord.state == Join():
            self.state = self.state.switchto("join")

    def platoon_mode(self, platoonvehicle):
        if self.state == Join() and self.follower_frontgapcoord.state == Platoon():
            self.state = self.state.switchto("platoon")

    def backsplit_mode(self, platoonvehicle):
        if self.state == Platoon and self.follower_frontgapcoord.state == Split():
            self.state = self.state.switchto("split")

    def backsplit_ego_mode(self, platoonvehicle):
        if (self.state == Platoon) and (platoonvehicle.split_request() == True):
            self.state = self.state.switchto("split")
            self.follower_frontgapcoord.state = (
                self.follower_frontgapcoord.state.switchto("split")
            )
