max_relative_speed = 0.1
max_gap_distance_error = 0.1
# standalone_gap=0
class Vehicle:
    """
        Vehicle object defining properties and methods required to store and compute predictions according to a vehicle model.

        Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

        Args:

            abscissa (float):   x coordinate [m],
            acceleration (float):   Acceleration [m/s2],
            distance (float):   Distance [m],
            vehid (int):   Unique vehicle identifier,
            ordinate (float):  y coorindate [m],
            link (str):  Link name,
            vehtype (str):  Vehicle type,
            speed (float):  speed [m/s],
            lane (int):  lane (from right to left),
            elevation (float):  elevation [m],
            dynamic (VehicleDynamic): Vehicle dynamics (check )
            itinerary (list):  list of ordered links in the network [list],

    """

    def __init__(
        self,
        abscissa=0,
        acceleration=0,
        distance=0,
        vehid=1,
        ordinate=0,
        link=1,
        vehtype=100,
        speed=0,
        lane=1,
        elevation=0,
    ):
        """ This initializer creates a Vehicle
        """
        self.abscissa = abscissa
        self.acceleration = acceleration
        self.distance = distance
        self.vehid = vehid
        self.ordinate = ordinate
        self.link = link
        self.vehtype = vehtype
        self.speed = speed
        self.lane = lane
        self.elevation = elevation

    def is_platoon_vehicle(self):
        if self.vehtype == 100:
            return True
        else:
            return False

    def __repr__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"



class PlatoonVehicle(Vehicle):
    """ This class is to store functionality of a platoon vehicle"""

    def __init__(
        self,
        leader_PCM_capable=True,
        follower_PCM_capable=True,
        leader_split_request=False,
        follower_split_request=False,
        ego_distance_gap_to_leader=0,
        leader_id=1,
        follower_id=-1,
        leader_speed=4.0,
        leader_length=5.0,
        gap_distance_error=0,
        ego_split_request=False,
        ego_standalone_time_gap=1,
        front_target_state="standalone",
        rear_target_state="standalone",
        leader_rear_target_state="standalone",
        follower_front_target_state="standalone",
        ego_speed=4.0,
        ego_position=0,
        leader_position=0,
        desired_gap=1,
        standalone_gap=1,
        platoon_id=1,
        platoon_length=1,
        front_id=2,
        intruder=False,
        ego_platoon_position=1,
        leader_platoon_position=2,
        maximum_platoon_length=7,
        platoon_desired_speed=50,
        platoon_desired_time_gap=2,
        max_connection_distance=100,
    ):
        self.leader_PCM_capable = leader_PCM_capable
        self.follower_PCM_capable = follower_PCM_capable
        self.leader_split_request = leader_split_request
        self.follower_split_request = follower_split_request
        self.ego_distance_gap_to_leader = ego_distance_gap_to_leader
        self.leader_id = leader_id
        self.follower_id = follower_id
        self.leader_speed = leader_speed
        self.leader_length = leader_length
        self.gap_distance_error = gap_distance_error
        self.ego_split_request = ego_split_request
        self.ego_standalone_time_gap = ego_standalone_time_gap
        self.front_target_state = front_target_state
        self.rear_target_state = rear_target_state
        self.leader_rear_target_state = leader_rear_target_state
        self.follower_front_target_state = follower_front_target_state
        self.ego_speed = ego_speed
        self.ego_position = ego_position
        self.leader_position = leader_position
        self.desired_gap = desired_gap
        self.standalone_gap = standalone_gap
        self.platoon_id = platoon_id
        self.platoon_length = platoon_length
        self.intruder = intruder
        self.front_id = front_id
        self.ego_platoon_position = ego_platoon_position
        self.leader_platoon_position = leader_platoon_position
        self.maximum_platoon_length = maximum_platoon_length
        self.max_connection_distance = max_connection_distance
        self.platoon_desired_speed = platoon_desired_speed
        self.platoon_desired_time_gap = platoon_desired_time_gap

    def relative_speed(self):
        speed_diff = self.speed - self.leader.speed
        return speed_diff

    # def gap_distance_error(self):
    #     gap = self.leader_position - self.ego_position - self.leader_length
    #     return gap

    def gap_distance_to_leader(self):
        gap = self.leader_position - self.ego_position - self.leader_length
        return gap

    # def desired_gap(self):
    #     gap = self.desi
    #     return gap

    def joinable(self):
        if (
            (self.leader_platoon_position < self.maximum_platoon_length)
            and (
                self.leader_platoon_position + self.platoon_length
                <= self.maximum_platoon_length
            )
            and (self.gap_distance_to_leader() < self.max_connection_distance)
            and self.leader_PCM_capable == True
            and (self.intruder == False)
            and (self.leader_split_request == False)
        ):  # add condition for vehicle split
            return True
        else:
            return False

    def join_request(self):
        if self.joinable() == True:
            return True
        else:
            return False
            # self.state = self.state.switchto("join")

    def cancel_join_request(self):  # add lane change and other conditions
        if self.joinable() == False:
            return True
        else:
            return False
            # self.state = self.state.switchto("standalone")

    def confirm_platoon(self):
        if (
            abs(self.ego_distance_gap_to_leader - self.desired_gap)
            < max_gap_distance_error
        ):
            return True
        else:
            return False
            # self.state = self.state.switchto("platoon")
            # self.ego_platoon_position = self.leader_platoon_position+ 1  # update position

    def platoon_split(self):
        if (
            (self.intruder == True)
            or (self.ego_split_request == True)
            or (self.leader_split_request == True)
        ):
            return True
        else:
            return False
            # self.state = self.state.switchto("split")

    # def platoon_front_split(self): # should be in front cordinator
    #     if (self.ego_split_request == True):
    #         return True
    #     elif leader_rear_state=='backsplit':
    #         return True
    #     else:
    #          return False
    #
    #
    # def platoon_back_split(self): # In the rear coordinator
    #     if (self.ego_split_request == True):
    #         return True
    #     elif follower_front_state=='frontsplit':
    #         return True
    #     else:
    #          return False
    #
    #             # self.state = self.state.switchto("split")

    def rejoin_platoon(self):
        if (
            self.intruder
            == False  # and (self.ego_distance_gap_to_leader <= self.standalone_gap)
        ):
            return True
        else:
            return False
            # self.state = self.state.switchto("platoon")

    def leave_platoon(self):
        if (
            self.ego_distance_gap_to_leader == self.standalone_gap
        ):  # distance to cutin vehicle
            return True
        else:
            return False
            # self.state = self.state.switchto("standalone")
