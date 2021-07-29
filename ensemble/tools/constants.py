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
    ``DCT_LIB_CACC``               Default CACC library path
    ============================  ======================================

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from datetime import date, datetime, timedelta
from numpy import array, float64, int32
import os, platform
import decouple
from decouple import UndefinedValueError
from pathlib import Path

# ============================================================================
# SPECIFIC  IMPORTS
# ============================================================================

from symupy.utils.constants import (
    DEFAULT_LIB_OSX,
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
    TOTAL_SIMULATION_STEPS,
    HOUR_FORMAT,
)

from ensemble.tools.exceptions import EnsembleAPIWarning, EnsembleAPIError

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
# Point to ini file
ini_config = decouple.Config(os.path.dirname(__file__))

DEFAULT_LIB_OSX = os.path.join(
    os.getenv("CONDA_PREFIX"), "lib", "libSymuVia.dylib"
)

DEFAULT_LIB_LINUX = os.path.join(
    os.getenv("CONDA_PREFIX"), "lib", "libSymuVia.so"
)

DEFAULT_LIB_WINDOWS = os.path.join(
    os.getenv("CONDA_PREFIX"), "lib", "libSymuVia.dll"
)

if platform.system() == "Darwin":
    try:
        if Path(DEFAULT_LIB_OSX).exists():
            DEFAULT_PATH_SYMUVIA = DEFAULT_LIB_OSX
        else:
            DEFAULT_PATH_SYMUVIA = ini_config("DEFAULT_LIB_OSX")
    except UndefinedValueError:
        EnsembleAPIWarning("No Simulator could be defined")
        DEFAULT_PATH_SYMUVIA = ""
elif platform.system() == "Linux":
    try:
        if Path(DEFAULT_LIB_LINUX).exists():
            DEFAULT_PATH_SYMUVIA = DEFAULT_LIB_LINUX
        else:
            DEFAULT_PATH_SYMUVIA = ini_config("DEFAULT_LIB_LINUX")
    except UndefinedValueError:
        EnsembleAPIWarning("No Simulator could be defined")
        DEFAULT_PATH_SYMUVIA = ""
elif platform.system() == "Windows":
    try:
        DEFAULT_PATH_SYMUVIA = ini_config("DEFAULT_LIB_WINDOWS")
    except UndefinedValueError:
        EnsembleAPIWarning("No Simulator could be defined")
        DEFAULT_PATH_SYMUVIA = ""
else:
    raise EnsembleAPIError("Platform could not be determined")

# Fill candidates
DCT_DEFAULT_PATHS = {
    ("symuvia", "Darwin"): DEFAULT_LIB_OSX,
    ("symuvia", "Windows"): DEFAULT_LIB_OSX,
    ("vissim", "Windows"): DEFAULT_LIB_WINDOWS,
    ("vissim", "Darwin"): DEFAULT_LIB_WINDOWS,
    ("symuvia", "Linux"): DEFAULT_LIB_LINUX,
    ("vissim", "Linux"): DEFAULT_LIB_LINUX,
}

# Dynamic Platoon Data

DCT_PLT_DATA = {
    "plt_id": 0,  # Platoon id
    "headway": [
        0.0,
    ],  # Inter-vehicle distance List[Float, Float]
    "plt_brands": [
        0,
    ],  # Vehicle Platoon brands List[Int, Int]
    "plt_order": [
        (0, 0),
    ],  # Vehicle id - brand List[Tuple[Int,Int]] head-tail order
}

DCT_LIB_CACC = {
    "Windows": "OperationalDLL.dll",
    "Darwin": "OperationalDLL.dylib",
    "Linux": "OperationalDLL.so",
}

DCT_LIB_TRUCK = {
    "Windows": "truckDynamics.dll",
    "Darwin": "truckDynamics.dylib",
    "Linux": "truckDynamics.so",
}

DEFAULT_CACC_PATH = os.path.join(
    os.getcwd(),
    "ensemble",
    "libs",
    platform.system().lower(),
    DCT_LIB_CACC[platform.system()],
)

DEFAULT_TRUCK_PATH = os.path.join(
    os.getcwd(),
    "ensemble",
    "libs",
    platform.system().lower(),
    DCT_LIB_TRUCK[platform.system()],
)


# *****************************************************************************
# SYMUVIA CONSTANTS
# *****************************************************************************

# *****************************************************************************
# VISSIM CONSTANTS
# *****************************************************************************

FIELD_FORMAT_VISSIM = {
    "CoordFrontX": float,
    "Acceleration": float,
    "Pos": float,
    "No": int,
    "CoordFrontY": float,
    "Lane\\Link\\No": str,
    "VehType": str,
    "Speed": lambda x: float(x) / 3.6,
    "Lane\\Index": int,
    "@z": float,
    "@etat_pilotage": bool,
}

FIELD_DATA_VISSIM = {
    "CoordFrontX": "abscissa",
    "Acceleration": "acceleration",
    "Pos": "distance",
    "No": "vehid",
    "CoordFrontY": "ordinate",
    "Lane\\Link\\No": "link",
    "VehType": "vehtype",
    "Speed": "speed",
    "Lane\\Index": "lane",
    "@z": "elevation",
    "@etat_pilotage": "driven",
}

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
