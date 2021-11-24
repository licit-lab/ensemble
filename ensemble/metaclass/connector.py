"""
Abstract Connector 
===================
This module implements a general metaclass for a connector.
"""


# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class AbsConnector(metaclass=abc.ABCMeta):
    # _c_iter = 0

    # def __repr__(self):
    #     return f"{self.__class__.__name__}({self.libraryname})"

    @abc.abstractproperty
    def simulation_step(self):
        """Current simulation iteration"""
        pass

    @abc.abstractproperty
    def get_vehicle_data(self):
        """List of dictionaries containing vehicle data"""
        pass

    @abc.abstractmethod
    def load_simulator(self):
        """Method to load the simulation platform"""
        pass

    @abc.abstractmethod
    def load_scenario(self, scenario: str):
        """Method to load simulation into simulator"""
        pass

    @abc.abstractmethod
    def register_simulation(self, scenarioPath: str):
        """Registers a scenario file into the simulator"""
        pass

    @abc.abstractmethod
    def request_answer(self):
        """Request answer from simulator"""
        pass

    @abc.abstractmethod
    def push_data(self):
        """Push data back to the simulator"""
        pass
