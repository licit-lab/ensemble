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
    ``DEFAULT_LIB_LINUX``          Default Linux library path  
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

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


# Default simulator per platform

# *****************************************************************************
# DEFAULT PATHS TO FIND SIMULATOR PLATFORMS
# *****************************************************************************

# DEFAULT_LIB_OSX = "/Users/ladino/Documents/03-Code/02-Python/libraries/symupy/lib/osx-64/libSymuVia.dylib"

DEFAULT_LIB_OSX = "/Users/andresladino/Documents/01-Code/04-Platforms/dev-symuvia/build/lib/libSymuVia.dylib"

DEFAULT_LIB_LINUX = "/home/build-symuvia/build/symuvia/libSymuVia.so"

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

DCT_DEFAULT_PATHS = {
    ("symuvia", "Darwin"): DEFAULT_LIB_OSX,
    ("symuvia", "Linux"): DEFAULT_LIB_LINUX,
    ("vissim", "Windows"): DEFAULT_LIB_WINDOWS,
}

# *****************************************************************************
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
    "abscisa": 0.0,  #  x coordinate [m]
    "acceleration": 0.0,  #  acceleration [m/s2]
    "distance": 0.0,  #  distance [m]
    "vehid": 0,  #  unique identifier [int]
    "ordinate": 0,  # y coorindate [m]
    "link": "",  # link [string]
    "veh_type": "",  # vehicle type [string1]
    "speed": 0.0,  # speed [m/s]
}

# Dynamic Platoon Data

DCT_PLT_DATA = {
    "plt_id": 0,  # Platoon id
    "headway": [0.0,],  # Inter-vehicle distance List[Float, Float]
    "plt_brands": [0,],  # Vehicle Platoon brands List[Int, Int]
    "plt_order": [(0, 0),],  # Vehicle id - brand List[Tuple[Int,Int]] head-tail order
}

# *****************************************************************************
# STREAM CONSTANTS
# *****************************************************************************

FIELD_DATA = {
    "@abs": "abscisa",
    "@acc": "acceleration",
    "@dst": "distance",
    "@id": "vehid",
    "@ord": "ordinate",
    "@tron": "link",
    "@type": "vehtype",
    "@vit": "speed",
    "@voie": "lane",
    "@z": "elevation",
}

FIELD_FORMAT = {
    "@abs": float,
    "@acc": float,
    "@dst": float,
    "@id": int,
    "@ord": float,
    "@tron": str,
    "@type": str,
    "@vit": float,
    "@voie": int,
    "@z": float,
}

FLOAT_SELECT = float64
INT_SELECT = int32

FIELD_FORMATAGG = {
    "abscisa": (array, FLOAT_SELECT),
    "acceleration": (array, FLOAT_SELECT),
    "distance": (array, FLOAT_SELECT),
    "vehid": (array, INT_SELECT),
    "ordinate": (array, FLOAT_SELECT),
    "link": (list, None),
    "vehtype": (list, None),
    "speed": (array, FLOAT_SELECT),
    "lane": (array, INT_SELECT),
    "elevation": (array, FLOAT_SELECT),
}


# *****************************************************************************
# SYMUVIA CONSTANTS
# *****************************************************************************

# *****************************************************************************
# CONNECTOR
# *****************************************************************************
# Buffer string size
BUFFER_STRING = 1000000

# *****************************************************************************
# SCENARIO
# *****************************************************************************
# Format time from xml file
HOUR_FORMAT = "%H:%M:%S"

# DATE/TIME INFORMATION
DELTA_TIME = timedelta(minutes=1)
TIME_STEP = timedelta(seconds=1).total_seconds()
today = date.today().strftime("%Y-%m-%d")
st_time = datetime.now()
ed_time = st_time + DELTA_TIME
st_time_str = st_time.strftime("%H:%M:%S")
ed_time_str = ed_time.strftime("%H:%M:%S")

DCT_SIMULATION_INFO = {
    "id": "simID",
    "pasdetemps": f"TIME_STEP",
    "debut": f"st_time_str",
    "fin": f"ed_time_str",
    "loipoursuite": "exacte",
    "comportementflux": "iti",
    "date": f"today",
    "titre": "default_simulation",
    "proc_deceleration": "false",
    "seed": "1",
}

# *****************************************************************************
# VISSIM CONSTANTS
# *****************************************************************************


# *****************************************************************************
# DATA VEHICLE DYNAMICS
# *****************************************************************************
ENGINE_CONSTANT = 0.2
