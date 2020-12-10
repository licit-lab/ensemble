# """
#     This module contains objects that implement the tactical control layer and communication towards the operational layer
# """

# # ============================================================================
# # INTERNAL IMPORTS
# # ============================================================================

# from ensemble.logic.frozen_set import SortedFrozenSet
# from .tactical.gapcordinator import FrontGap, RearGap

# # ============================================================================
# # CLASS AND DEFINITIONS
# # ============================================================================


# class MultiBrandPlatoonRegistry(SortedFrozenSet):
#     """
#         This class models and represents a single platoon registry
#     """

#     def __init__(self):
#         self.gap_coord = {coordtype: dict() for coordtype in ("FGC", "RGC")}

#     def registerTruck(self, vehicle):
#         """ Registers a new candidate for platoon
#         """
#         self.cap_coord["FGC"][vehicle.id] = FrontGap(vehicle)
#         self.cap_coord["RGC"][vehicle.id] = RearGap(vehicle)

#     def unregisterTruck(self, vehicle):
#         """ Unregister exisiting truck
#         """
#         del self.cap_coord["FGC"][vehicle.id]
#         del self.cap_coord["RGC"][vehicle.id]

#     def update_truck_registry(self, request):
#         """ Update truck registry by registering / deregistering
#         """
#         for key, vehicle in request.vehicles.items():
#             if vehicle not in self:
#                 self.regiserTruck(vehicle)

#     def __contain__(self, vehicle):
#         """ Check if element has created
#         """
#         return (vehicle.id in self.cap_coord["FGC"].keys()) & (
#             vehicle.id in self.cap_coord["RGC"].keys()
#         )


# class MultiBrandPlatoonClient(object):
#     def __init__(self):
#         pass
