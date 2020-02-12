# Here we describe how we think the structure of the joint algorithm should be.
#The two simulators are called and started sepeartely  and they both perform different tasks
# Each should be capable of sending and retrieving network and status data
# Some Tasks are simulator  dependent(e.g. retrieving data) while others are simulator independent(l e.g oop through all vehicles)


Simulator = 1  # 1 stands for vissim 2 stands for symivuvia

# open simulator
if Simulator ==1:
    # Start vissim instance
    # Import COM-Server and os
    import win32com.client as com
    import os
    Vissim = com.gencache.EnsureDispatch("Vissim.Vissim-64.10")  # Vissim 10 - 64 bit version
    # Load Vissim Network
    NetworkPath = 'C:\\Users\\Public\\Documents\\GLOSA\\GlosaTrafficLight' # The path to network
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.inpx') # Join Path and FileName
    flag_read_additionally = False  # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(Filename, flag_read_additionally)
    # Load a Layout:
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.layx')
    Vissim.LoadLayout(Filename)


if simulator == 2:
    # andres start symuvia here
    L=symuvia(x)


# retrieve network data and status data




#start sim here
if simulator == 1:
    Vissim.Simulation.RunSingleStep()
    simulaton_runtime = Vissim.Simulation.AttValue('SimPeriod')

if simulator == 2:
    null

for i in range(start_simulation,end_simulation,time_step):
    # retrieve data (simulator dependent)
    if Simulator == 1:
     All_Vehicles = Vissim.Net.Vehicles.GetAll()  # get all vehicles in the network at the actual simulation second
     Vehicle = All_Vehicles[0] # First Vehicle in List
     VehicleLane = Vehicle.Lane # Lane of first vehicle
     VehicleSignalHead=VehicleLane.SigHeads # SignalHeads in that lane
     VehicleSpeed= Vehicle.AttValue('Speed') # Vehicle current speed
    Nveh = len(All_Vehicles) # Number of vehicle in the network


    if simulator == 2:
     Nveh = Len
     symuvia.net.vehicles

    for i in range( Nveh): #loop over all vehicles (simulator independent)
        # Nveh Joined algorithmusing a joined structure
        vehKm = Nveh * distance_travelled  # Calculating Vehkm  using number of vehicles(Nveh)  as input
        # send back the data to the vehicle
        #  For example Set Desired Speed of  a vehicle:
        DesSpeed_new = 30  # The desired speed you want to send
        link_number = 1  # The link
        lane_number = 1  # and lane
        link_coordinate = 70  # and the position in the link

        # sent data back (sim depend)
        if simulator == 1:
            # use vissim to send back data
            Vehicle.SetAttValue('DesSpeed', DesSpeed_new)
            # Move a vehicle:
            Vehicle.MoveToLinkPosition(link_number, lane_number, link_coordinate)
        if simulator == 2:
            # use Symuvia to sent backdata
            Symuvia('DesSpeed', DesSpeed_new)

    # end timestep, start new timestep (simulation  dependent)









