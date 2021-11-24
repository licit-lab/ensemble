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
    # @abc.abstractproperty
    # def ego(self):
    #     """Ego vehicle information"""
    #     pass

    @abc.abstractproperty
    def joinable(self):
        """Indicates if the coordinator is joinable"""
        pass

    @abc.abstractmethod
    def cancel_join_request(self, value):
        """Determines if a join request needs to be cancelled"""
        pass

    @abc.abstractproperty
    def dv(self):
        """Differential speed @current time"""
        pass

    @abc.abstractproperty
    def dx(self):
        """Headway space @current time"""
        pass

    @abc.abstractproperty
    def ttd(self):
        """Total travel distance @current time"""
        pass

    @abc.abstractproperty
    def speed(self):
        """Speed @current time"""
        pass

    @abc.abstractproperty
    def acceleration(self):
        """Acceleration @current time"""
        pass

    @abc.abstractproperty
    def x(self):
        """Distance on link @current time"""
        pass

    @abc.abstractproperty
    def vehid(self):
        """Vehicle identifier"""
        pass

    @abc.abstractproperty
    def control(self):
        """Applied control @current time"""
        pass

    @abc.abstractproperty
    def status(self):
        """Platoon status @current time"""
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

    @abc.abstractproperty
    def history_state(self):
        """Historical status"""
        pass

    @abc.abstractproperty
    def history_control(self):
        """Historical control"""
        pass

    @abc.abstractproperty
    def history_reference(self):
        """Historical control"""
        pass

    @abc.abstractmethod
    def get_step_data(self) -> tuple:
        """Get single step data"""
        pass
