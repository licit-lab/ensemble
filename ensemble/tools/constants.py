"""
    This module contains a **constants** and **default** parameters. These parameters can be accessed    at any time by whatever of the modules. 

    Some of the values here will be used to parametrize simulations to multiple platforms and some for specific ones. Specific zones within the source code have been marked to place the corresponding constant values.  Please, use uppercase letters for defining new constant values. 

    Example:
        To use the ``Constants`` import the module as::

            >>> import ensemble.tools.constants as ct
            >>> ct.BUFFER_STRING # access the buffer size 


    ============================  ======================================
     **Variable**                 **Description**
    ----------------------------  --------------------------------------
    ``BUFFER_STRING``              Buffer size
    ``DEFAULT_LIB_OSX``            Default OS X library path (SymuVia)
    ``DEFAULT_LIB_LINUX``          Default Linux library path  (SymuVia)
    ``DEFAULT_LIB_WINDOWS``        Default Windows library path (Vissim)
    ``DCT_SIMULATORS``             Simulator according to SO 
    ``DCT_DEFAULT_PATHS``          Available combinations SO/simulator
    ``DCT_RUNTIME_PARAM``          Runtime default parameters 
    ``DCT_VEH_PARAM``              Vehicle default parameters 
    ``DCT_VEH_DATA``               Vehicle data default parameters
    ``DCT_PLT_DATA``               Platoon parameters
    ============================  ======================================

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from datetime import date, datetime, timedelta
from numpy import array, float64, int32
import os

# ============================================================================
# SPECIFIC  IMPORTS
# ============================================================================

from symupy.utils.constants import (
    DEFAULT_LIB_OSX,
    DEFAULT_LIB_LINUX,
    DCT_DEFAULT_PATHS,
    FIELD_DATA,
    FIELD_FORMAT,
    FIELD_FORMATAGG,
    BUFFER_STRING,
    DCT_SIMULATION_INFO,
    DCT_EXPORT_INFO,
    DCT_TRAFIC_INFO,
    DCT_NETWORK_INFO,
    DCT_SCENARIO_INFO,
    TP_VEHTYPES,
    TP_VEHTYPES,
    TIME_STEP,
    ENGINE_CONSTANT,
    WRITE_XML,
    TRACE_FLOW,
    LAUNCH_MODE,
    TOTAL_SIMULATION_STEPS
)

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

# Vissim Command
DEFAULT_LIB_WINDOWS = "Vissim.Vissim-64.10"

# *****************************************************************************
# DEFAULT SIMULATOR/ OS ASSOCIATION
# *****************************************************************************

DCT_SIMULATORS = {
    "Darwin": "symuvia",
    "Linux": "symuvia",
    "Windows": "vissim",
}

# Feasible Simulator/Platform Paths/Libs

# Adding case for Vissim
DCT_DEFAULT_PATHS[("vissim", "Windows")] = DEFAULT_LIB_WINDOWS

# Dynamic Platoon Data

DCT_PLT_DATA = {
    "plt_id": 0,  # Platoon id
    "headway": [0.0,],  # Inter-vehicle distance List[Float, Float]
    "plt_brands": [0,],  # Vehicle Platoon brands List[Int, Int]
    "plt_order": [(0, 0),],  # Vehicle id - brand List[Tuple[Int,Int]] head-tail order
}

# *****************************************************************************
# SYMUVIA CONSTANTS
# *****************************************************************************

# *****************************************************************************
# VISSIM CONSTANTS
# *****************************************************************************

# *****************************************************************************
# ENSEMBLE
#
# DEFAULT SCENARIO PARAMETERS
# *****************************************************************************

# Runtime Parameters

DCT_RUNTIME_PARAM = {
    "sampling_time": 1,
    "total_steps": 60,
    "sampling_time_operational": 1 / 10,
    "sampling_time_tactical": 5,
}

# Vehicles Parameters

DCT_VEH_PARAM = {
    "mass": 1,  # Mass [Kg]
    "lenght": 1,  # Vehicle length [m]
    "max_speed": 25,  # Maximum Vehicle speed [m/s]
    "cong_speed": -6.25,  # Vehicle speed [m/s]
}

# Dynamic Vehicle Data

DCT_VEH_DATA = {
    "abscissa": 0.0,  #  x coordinate [m]
    "acceleration": 0.0,  #  acceleration [m/s2]
    "distance": 0.0,  #  distance [m]
    "vehid": 0,  #  unique identifier [int]
    "ordinate": 0,  # y coorindate [m]
    "link": "",  # link [string]
    "vehtype": "",  # vehicle type [string1]
    "speed": 0.0,  # speed [m/s]
    "lane": 1,  # lane (from right to left) [int]
    "elevation": 0.0,  # elevation m
    "itinerary": [],  # list of ordered links in the network [list]
}

# Platoon parameters

DCT_PLT_CONST = {
    "max_platoon_length": 7,  # maximum number of vehicles allowed in platoon
    "max_connection_distance": 100,  # maximum distance for communication(metres)
}

if __name__ == "__main__":
    print(os.environ.get("SYMUVIALIB"))
