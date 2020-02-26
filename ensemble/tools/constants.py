# Constant values

# Default simulator per platform

# -------------------------------------- DEFAULT PATHS TO FIND SIMULATOR PLATFORMS--------------------------------------

DEFAULT_LIB_OSX = "/Users/ladino/Documents/03-Code/02-Python/libraries/symupy/lib/osx-64/libSymuVia.dylib"

DEFAULT_LIB_LINUX = "/home/build-symuvia/build/symuvia/libSymuVia.so"

DEFAULT_LIB_WINDOWS = "Vissim.Vissim-64.10"

# ------------------------------------- DEFAULT SIMULATOR/ OS ASSOCIATION ----------------------------------------------

DCT_SIMULATORS = {
    "Darwin": "symuvia",
    "Linux": "symuvia",
    "Windows": "vissim",
}

# Feasible Simulator/Platform Paths/Libs

DCT_DEFAULT_PATHS = {
    ("symuvia", "Darwin"): DEFAULT_LIB_OSX,
    ("symuvia", "Linux"): DEFAULT_LIB_LINUX,
    ("visim", "Windows"): DEFAULT_LIB_WINDOWS,
}

# -------------------------------------- DEFAULT SCENARIO PARAMETERS ---------------------------------------------------

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
