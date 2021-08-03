

from ensemble.component.vehicle import Vehicle
from ensemble.handler.symuvia.stream import SimulatorRequest


# TODO: Check constructor alternatives
req = SimulatorRequest()
v1 = Vehicle(req, vehid=0)
