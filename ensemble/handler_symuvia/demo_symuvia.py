# Input: simulator path (Relative/Absolute)
simulator_path = "libSymuVia.dylib"

# Input: Scenario (Network + Demand + Control)
scenario_file = "scenario.xml"

from ctypes import cdll, c_int, byref, c_bool, create_string_buffer

# Charge library into python
symuvia = cdll.LoadLibrary(simulator_path)

# Create an instance for the simulation (0 = success)
status = symuvia.SymLoadNetworkEx(simulator_path.encode("UTF8"))

# Generate buffers
sRequest = create_string_buffer(10000)  # Data queries
bEnd = c_int()  # Boolean to stop simululation
bTrace = c_bool(False)  # Store traces in XML

# Step by step
bContinue = True
while bContinue:
    bSuccess = symuvia.SymRunNextStepEx(sRequest, bTrace, byref(bEnd))
    data = sRequest.value  # Retrieve info right after executing step

# other methods
# symuvia.SymCreateVehicleEx # Create a vehicle of a specific predefined type
# symuvia.SymDriveVehicleEx # Modifies position of a vehicle (longitudinal/lateral)
