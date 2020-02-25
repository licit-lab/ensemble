# Constant values

# Default simulator per platform

DEFAULT_LIB_OSX = "/Users/ladino/Documents/03-Code/02-Python/libraries/symupy/lib/osx-64/libSymuVia.dylib"

DEFAULT_LIB_LINUX = "/home/build-symuvia/build/symuvia/libSymuVia.so"

DEFAULT_LIB_WINDOWS = "Vissim.Vissim-64.10"


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

DCT_PARAMETERS = {
    "sampling_time": 1,
    "total_steps": 60,
    "sampling_time_operational": 1 / 10,
    "sampling_time_tactical": 5,
}
