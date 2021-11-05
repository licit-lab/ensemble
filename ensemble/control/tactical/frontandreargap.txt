from ensemble.component.platoonvehicleinfo import PlatoonVehicle

max_relative_speed = 0.1
max_gap_distance_error = 0.1
standalone_gap = 0
# max_connection_distance=100


class StandAlone:
    """
    The state which declares the vehicle in stand alone mode.
    A vehicle can move from StandAlone to Join
    """

    def run(self, veh):
        veh.front_target_state = "standalone"
        print("StandAloneMode")
        return self

    def run_rear(self, veh):
        veh.rear_target_state = "standalone"
        print("StandAloneMode")
        return self

    def next_state(self, veh):
        if veh.join_request() == True:
            # start collecting platoon information[Platoonid,frontid etc]
            return Join()
        else:
            return self


class Join:
    """
    The state which declares the vehicle in joining a platoon.
    A vehicle can move from Join state to platoon state
    """

    def run(self, veh):
        veh.front_target_state = "join"
        print("JoinMode")
        return self

    def run_rear(self, veh):
        veh.rear_target_state = "join"
        print("JoinMode")
        return self

    def next_state(self, veh):
        if veh.cancel_join_request() == True:
            # empty platoon information[Platoon id=0,frontid=0 etc]
            return StandAlone()
        elif veh.confirm_platoon() == True:
            # self.state = "platoon"  # update  vehicle state
            veh.ego_platoon_position = (
                veh.leader_platoon_position + 1
            )  # update position
            return Platoon()
        else:
            return self


class Platoon:
    """
    The state which declares the vehicle in a platoon
    A vehicle can move from platoon to split because of  cut-in(intruder) or to a split(requested  by ego vehicle or front target)
    """

    def run(self, veh):
        veh.front_target_state = "platoon"
        veh.ego_platoon_position = veh.leader_platoon_position + 1
        print("PlatoonMode")
        return self

    def run_rear(self, veh):
        veh.rear_target_state = "platoon"
        print("PlatoonMode")
        return self

    def next_state(self, veh):
        if (
            (veh.ego_split_request == True)
            or (veh.leader_split_request == True)
            or (veh.leader_rear_target_state == "backsplit")
        ):  # ask LIn
            # self.state = "frontsplit"  # update  vehicle state
            return FrontSplit()
        elif veh.intruder == True:
            return Cutin()
        else:
            return self

    def next_state_rear(self, veh):
        if (veh.ego_split_request == True) or (
            veh.follower_front_target_state == "frontsplit"
        ):
            # self.state = "backsplit"  # update  vehicle state
            return BackSplit()
        else:
            return self


class Cutin:
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def run(self, veh):
        veh.front_target_state = "cutin"
        print("CutInMode")
        return self

    def next_state(self, veh):

        if veh.rejoin_platoon() == True:
            # self.state = "platoon"  # update  vehicle state
            return Platoon()
        elif veh.leave_platoon() == True:
            # self.state = "standalone"  # update  vehicle state
            return FrontSplit()
        else:
            return self


class FrontSplit:
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def run(self, veh):
        veh.front_target_state = "frontsplit"
        print("FrontSplitMode")
        return self

    def run_rear(self, veh):
        veh.rear_target_state = "frontsplit"
        print("FrontSplitMode")
        return self

    def next_state(self, veh):

        if veh.leave_platoon() == True:
            # empty platoon information[Platoon id=0,frontid=0 etc]
            return StandAlone()

        else:
            return self


class BackSplit:
    """
    The state which declares the vehicle splitting from platoon
    A vehicle can move from split to platoon or to standalone
    """

    def run(self, veh):
        veh.front_target_state = "backsplit"
        print("BackSplitMode")
        return self

    def run_rear(self, veh):
        veh.rear_target_state = "backsplit"
        print("BackSplitMode")
        return self

    def next_state(self, veh):

        if veh.leave_platoon() == True:
            # self.state = "standalone"  # update  vehicle state
            return StandAlone()
        else:
            return self


class FrontGapState:
    def __init__(self, veh):
        if veh.front_target_state == "standalone":
            self.currentState = StandAlone()
            self.currentState.run(veh)
        elif veh.front_target_state == "join":
            self.currentState = Join()
            self.currentState.run(veh)
        elif veh.front_target_state == "platoon":
            self.currentState = Platoon()
            self.currentState.run(veh)
        elif veh.front_target_state == "cutin":
            self.currentState = Cutin()
            self.currentState.run(veh)
        else:
            self.currentState = FrontSplit()
            self.currentState.run(veh)

    def update_state(self, veh):
        self.currentState = self.currentState.next_state(veh)
        self.currentState.run(veh)


class RearGapState:
    def __init__(self, veh):
        if veh.rear_target_state == "standalone":
            self.currentState = StandAlone()
            self.currentState.run_rear(veh)
        elif veh.rear_target_state == "join":
            self.currentState = Join()
            self.currentState.run_rear(veh)
        elif veh.rear_target_state == "platoon":
            self.currentState = Platoon()
            self.currentState.run_rear(veh)
        else:
            self.currentState = BackSplit()
            self.currentState.run_rear(veh)

    def update_state(self, veh):
        if veh.follower_front_target_state == "standalone":
            self.currentState = StandAlone()
            self.currentState.run_rear(veh)
        elif veh.follower_front_target_state == "join":
            self.currentState = Join()
            self.currentState.run_rear(veh)
        elif (
            veh.follower_front_target_state == "platoon"
            or veh.rear_target_state == "platoon"
        ):
            self.currentState = Platoon()
            self.currentState = self.currentState.next_state_rear(veh)
            self.currentState.run_rear(veh)
        elif (
            veh.follower_id == -1
            or veh.follower_front_target_state == -1
            or veh.follower_PCM_capable == False
        ):
            self.currentState = StandAlone()
            self.currentState.run_rear(veh)
        else:
            self.currentState = BackSplit()
            self.currentState.run_rear(veh)
        # self.currentState = self.currentState.next_state(veh)
        # self.currentState.run(veh)


veh = PlatoonVehicle(
    leader_PCM_capable=1,
    leader_split_request=False,
    ego_distance_gap_to_leader=0,
    leader_id=1,
    leader_speed=4.0,
    leader_length=5.0,
    gap_distance_error=0,
    ego_split_request=False,
    ego_standalone_time_gap=1,
    front_target_state="join",
    ego_speed=4.0,
    ego_position=0,
    leader_position=0,
    desired_gap=1,
    standalone_gap=1,
    platoon_id=1,
    platoon_length=1,
    front_id=2,
    intruder=True,
    ego_platoon_position=1,
    leader_platoon_position=2,
    maximum_platoon_length=7,
    platoon_desired_speed=50,
    platoon_desired_time_gap=2,
    max_connection_distance=100,
)
fgc = FrontGapState(veh)
print(fgc.update_state(veh))
print(fgc.currentState)
print(veh.front_target_state)
