"""
Abstract Gap Coordinator 
========================
This module implements a general metaclass for a vehicle gap coordinator.
"""


# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class AbsSingleGapCoord(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def joinable(self):
        """Indicates if the coordinator is joinable"""
        pass

    @abc.abstractmethod
    def cancel_join_request(self, value):
        """Determines if a join request needs to be cancelled"""
        pass

    @abc.abstractproperty
    def ttd(self):
        """Total travel distance"""
        pass

    @abc.abstractproperty
    def x(self):
        """Distance on link"""
        pass

    @abc.abstractproperty
    def vehid(self):
        """Vehicle identifier"""
        pass

    @abc.abstractproperty
    def status(self):
        """Platoon status"""
        pass

    @abc.abstractproperty
    def platoon(self):
        """Platoon enabled"""
        pass

    @abc.abstractproperty
    def comv2x(self):
        """Communication availability"""
        pass

    @abc.abstractproperty
    def positionid(self):
        """Position within the platoon"""
        pass
