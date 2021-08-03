"""
Abstract Dynamics 
===================
This module implements a general metaclass for the dynamics.
"""


# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class AbsDynamics(metaclass=abc.ABCMeta):

    
    @abc.abstractproperty
    def T(self):
        """Current time step"""
        pass

    @abc.abstractmethod
    def __call__(self):
        """Callable Dynamics"""
        pass
