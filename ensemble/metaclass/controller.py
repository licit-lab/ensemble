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
# CLASS AND DEFINITIONS
# ============================================================================


class AbsController(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, leader, ego, r_ego, t, T):
        pass
