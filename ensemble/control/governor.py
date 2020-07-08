"""
    This module contains objects that implement the tactical control layer and communication towards the operational layer
"""

from .tactical.gapcordinator import FrontGap, RearGap


class MultiBrandPlatoonRegistry:
    """
        This 
    """
    def __init__(self):
        self.gap_coord = {coordtype: dict() for coordtype in ("FGC", "RGC")}

    def registerTruck(self, vehicle):
        """ Registers a new candidate for platoon
        """
        self.cap_coord["FGC"][vehicle.id] = FrontGap(vehicle)
        self.cap_coord["RGC"][vehicle.id] = RearGap(vehicle)

    def unregisterTruck(self, vehicle):
        """ Unregister exisiting truck 
        """
        del self.cap_coord["FGC"][vehicle.id]
        del self.cap_coord["RGC"][vehicle.id]


class MultiBrandPlatoonClient(object):
    def __init__(self):
        pass
