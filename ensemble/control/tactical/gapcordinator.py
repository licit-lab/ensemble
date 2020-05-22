from ensemble.state.platoontracker import StandAlone, Platoon, Join, Split
from ensemble.state.statemachine import StateMachine
from ensemble.component.platoonvehicle import  PlatoonVehicle
class FrontGap(StateMachine):
    def __init__(self,veh=PlatoonVehicle()):
        if veh.state=='STANDALONE':
         self.currentState=StandAlone()
        elif veh.state=='JOIN':
            self.currentState =Join()
        elif veh.state=='PLATOON':
            self.currentState =Platoon()
        else:
            self.currentState = Split()
class RearGap(StateMachine):
    def __init__(self,veh=PlatoonVehicle()):
        if veh.follower().state=='STANDALONE':
         self.currentState=StandAlone()
        elif veh.follower().state=='JOIN':
            self.currentState =Join()
        elif veh.follower().state=='PLATOON':
            self.currentState =Platoon()
        else:
            self.currentState = Split()