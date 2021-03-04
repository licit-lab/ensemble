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
    ``DEFAULT_PATH_SYMUVIA``       Default Path Towards SymuVia    
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
    ``FIELD_DATA``                 Vehicle trajectory data
    ``FIELD_FORMAT``               Trajectory data types
    ``HOUR_FORMAT``                Time format
    ``FIELD_FORMATAGG``            Format aggretations
    ``DCT_SIMULATION_INFO```       XML Simulation information
    ``DCT_EXPORT_INFO``            XML Export information
    ``DCT_TRAFIC_INFO``            XML Traffic information
    ``DCT_NETWORK_INFO``           XML Network information
    ``DCT_SCENARIO_INFO``          XML Scenario information
    ``TP_VEHTYPES``                Vehicle type information
    ``TP_ACCEL``                   Vehicle acceleration boundaries    
    ============================  ======================================

"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
from datetime import date, datetime, timedelta
import platform
import decouple
from decouple import UndefinedValueError, config, RepositoryIni
from numpy import array, float64, int32
from pathlib import Path
from collections import defaultdict

# ============================================================================
# SPECIFIC  IMPORTS
# ============================================================================

from ensemble.tools.exceptions import EnsembleAPIWarning, EnsembleAPIError

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================
SYSTEM = platform.system()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(BASE_DIR, "settings.ini")

config = decouple.Config(RepositoryIni(FILE_DIR))

# Solving conda (local,RTD)
RTDPATH = config("RTD_ENV", cast=str)
CONDA_PREFIX = os.getenv("CONDA_PREFIX", RTDPATH)

PATHS_2_SEARCH = (CONDA_PREFIX,)

# Default names/platform
DCT_LIBOSNAME = {
    "Darwin": "libSymuVia.dylib",
    "Linux": "libSymuVia.so",
    "Windows": "Vissim.Vissim-64.10",
}


def find_path(roots):
    for root in roots:
        if (p := Path(root)).is_dir():
            yield from p.glob(f"**/{DCT_LIBOSNAME[SYSTEM]}")


DEFAULT_PATH_SYMUVIA = ""
for path in find_path(PATHS_2_SEARCH):
    DEFAULT_PATH_SYMUVIA = (
        path if SYSTEM != "Windows" else DCT_LIBOSNAME[SYSTEM]
    )

print(f"Default path: {DEFAULT_PATH_SYMUVIA}")

# *****************************************************************************
# DEFAULT SIMULATOR/ OS ASSOCIATION
# *****************************************************************************

DCT_SIMULATORS = {
    "Darwin": "symuvia",
    "Linux": "symuvia",
    "Windows": "vissim",
}

# Feasible Simulator/Platform Paths/Libs

# Fill candidates
DCT_DEFAULT_PATHS = {
    ("symuvia", "Darwin"): DEFAULT_PATH_SYMUVIA,
    ("symuvia", "Windows"): DEFAULT_PATH_SYMUVIA,
    ("vissim", "Windows"): DEFAULT_PATH_SYMUVIA,
    ("vissim", "Darwin"): DEFAULT_PATH_SYMUVIA,
    ("symuvia", "Linux"): DEFAULT_PATH_SYMUVIA,
    ("vissim", "Linux"): DEFAULT_PATH_SYMUVIA,
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

DEFAULT_CACC_PATH = os.path.join(
    os.getcwd(),
    "ensemble",
    "libs",
    platform.system().lower(),
    DCT_LIB_CACC[platform.system()],
)


# =============================================================================
# DATA SYMUVIA
# =============================================================================

# =============================================================================
# STREAM CONSTANTS
# =============================================================================

BUFFER_STRING = 1000000
WRITE_XML = False
TRACE_FLOW = False
LAUNCH_MODE = "lite"
TOTAL_SIMULATION_STEPS = 0

FIELD_DATA = {
    "@abs": "abscissa",
    "@acc": "acceleration",
    "@dst": "distance",
    "@id": "vehid",
    "@ord": "ordinate",
    "@tron": "link",
    "@type": "vehtype",
    "@vit": "speed",
    "@voie": "lane",
    "@z": "elevation",
    "@etat_pilotage": "driven",
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
    "@etat_pilotage": bool,
}

FLOATFORMAT = float64
INTFORMAT = int32

FIELD_FORMATAGG = {
    "abscisa": (array, FLOATFORMAT),
    "acceleration": (array, FLOATFORMAT),
    "distance": (array, FLOATFORMAT),
    "vehid": (array, INTFORMAT),
    "ordinate": (array, FLOATFORMAT),
    "link": (list, None),
    "vehtype": (list, None),
    "speed": (array, FLOATFORMAT),
    "lane": (array, INTFORMAT),
    "elevation": (array, FLOATFORMAT),
}

# =============================================================================
# XML Data
# =============================================================================

# DATE/TIME INFORMATION
HOUR_FORMAT = "%H:%M:%S"
DELTA_TIME = timedelta(minutes=1)
TIME_STEP = timedelta(seconds=1).total_seconds()
TODAY = date.today().strftime("%Y-%m-%d")
ST_TIME = datetime.now()
ED_TIME = ST_TIME + DELTA_TIME
ST_TIME_STR = ST_TIME.strftime("%H:%M:%S")
ED_TIME_STR = ED_TIME.strftime("%H:%M:%S")

# SIMULATION INFORMATION
DCT_SIMULATION_INFO = {
    "id": "simID",
    "pasdetemps": f"{TIME_STEP}",
    "debut": f"ST_TIME_STR",
    "fin": f"ED_TIME_STR",
    "loipoursuite": "exacte",
    "comportementflux": "iti",
    "date": f"today",
    "titre": "default_simulation",
    "proc_deceleration": "false",
    "seed": "1",
}

# DATA EXPORT INFORMATION
DCT_EXPORT_INFO = {
    "trace_route": "false",
    "trajectoires": "true",
    "debug": "false",
    "debug_matrice_OD": "false",
    "debug_SAS": "false",
    "csv": "true",
}

# TAFFIC INFORMATION
DCT_TRAFIC_INFO = {
    "id": "trafID",
    "accbornee": "true",
    "coeffrelax": "4",
    "chgtvoie_ghost": "false",
}

# NETWORK INFORMATION
DCT_NETWORK_INFO = {"id": "resID"}

# SCENARIO INFORMATION
DCT_SCENARIO_INFO = {
    "id": "defaultScenario",
    "simulation_id": DCT_SIMULATION_INFO.get("id"),
    "trafic_id": DCT_TRAFIC_INFO.get("id"),
    "reseau_id": DCT_NETWORK_INFO.get("id"),
    "dirout": "data",
    "prefout": "simout_ring_data",
}


TP_VEHTYPES = (
    {"id": "HDV", "w": "-5", "kx": "0.12", "vx": "25"},
    {"id": "CAV", "w": "-5", "kx": "0.12", "vx": "25"},
)

TP_ACCEL = (
    {"ax": "1.5", "vit_sup": "5.8"},
    {"ax": "1", "vit_sup": "8"},
    {"ax": "0.5", "vit_sup": "infini"},
)
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
    "max_connection_distance": 100,  # maximum distance for communication
    "platoon_types": ("PL", 201),
}

# =============================================================================
# CONTROL
# =============================================================================

BUFFER_CONTROL = 10  # Amount of control samples stored in memory

# =============================================================================
# VEHICLE DYNAMICS
# =============================================================================

ENGINE_CONSTANT = 0.2

# =============================================================================
# COMMUNICATION
# =============================================================================

RADIOUS_ANT = 500

if __name__ == "__main__":
    print(DEFAULT_PATH_SYMUVIA)
