from ensemble.control.operational import CACC
from ensemble.component.vehicle import Vehicle
from ensemble.handler.symuvia.stream import SimulatorRequest
from ensemble.component.vehiclelist import VehicleList

req = SimulatorRequest()

ego = Vehicle(req, veh_id=1)
leader = Vehicle(req, veh_id=0)

v1 = VehicleList(req)
v1.update_list(optional=[leader, ego])

c = CACC()

