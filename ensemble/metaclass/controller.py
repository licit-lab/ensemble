"""
Abstract Controller
===================
This module implements a general metaclass for the operatinonal controller.
"""


# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class AbsController(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __call__(self, ego, reference, t: float, T: float):
        pass
