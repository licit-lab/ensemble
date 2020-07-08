"""
    **Platoon Gap Coordinator**

    This module details the implementation of the ``Front Gap`` and ``Rear Gap`` Coordinators existing in each one of the vehicles created when running a platoon. The coordinators have access to a centralized information center called ``Data Query`` to retrieve information in the vecinity of the vehicle.

"""

from ensemble.state.platoontracker import StandAlone, Platoon, Join, Split
from ensemble.state.statemachine import StateMachine
from ensemble.component.platoonvehicle import PlatoonVehicle


class Subscriber:
    """
        This models the subscriber pattern that can be used by the publisher in order to receive information.
    """

    def __init__(self, name):
        self.name = name

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))

    def getegoinfo(self):
        pass


class FrontGap(Subscriber, StateMachine):
    def __init__(self, veh=PlatoonVehicle()):
        if veh.state == "STANDALONE":
            self.currentState = StandAlone()
        elif veh.state == "JOIN":
            self.currentState = Join()
        elif veh.state == "PLATOON":
            self.currentState = Platoon()
        else:
            self.currentState = Split()

    def update_states(self, vehicle_env):
        """ update informatino from ego vehicle + leader"""
        self.ego = vehicle_env['ego']
        self.leader = vehicle_env['leader']

class RearGap(Subscriber, StateMachine):
    def __init__(self, veh=PlatoonVehicle()):
        if veh.follower().state == "STANDALONE":
            self.currentState = StandAlone()
        elif veh.follower().state == "JOIN":
            self.currentState = Join()
        elif veh.follower().state == "PLATOON":
            self.currentState = Platoon()
        else:
            self.currentState = Split()
