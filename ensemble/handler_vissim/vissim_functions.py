import os
import json
import itertools
import pandas as pd
import time
import win32com.client as com
import os
import numpy as np
def load_vissim_network(NetworkPath,FileName,LayoutName):
    print('Hello Vissim SImulation  is Starting again')
    Vissim = com.gencache.EnsureDispatch("Vissim.Vissim-32.10")  # Vissim 10 - 64 bit
    #GlosaNetworkPath = 'C:\\Users\\Public\\Documents\\GLOSA\\GlosaTrafficLight'
    FileName = os.path.join(NetworkPath, FileName)
    flag_read_additionally = False  # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(FileName, flag_read_additionally)
    ## Load a Layout:
    LayoutName = os.path.join(NetworkPath,LayoutName)
    Vissim.LoadLayout(LayoutName)
    print('Vissim Network is now Loaded')
    return Vissim

def load_simulation_parameters(Vissim,simulation_parameters):
    End_of_simulation = simulation_parameters[0]  # simulation second [s]
    Simulation_Resolution = simulation_parameters[1]  # simulation second [s]
    Number_Runs = simulation_parameters[2]
    Simulation_Period = simulation_parameters[3]
    Vissim.Simulation.SetAttValue('SimRes', Simulation_Resolution)
    Vissim.Simulation.SetAttValue('NumRuns', Number_Runs)
    Vissim.Simulation.SetAttValue('SimPeriod', Simulation_Period)
    print('Simulation Parameters Now Loaded')
    return
def run_vissim_simulation(Vissim,simulation_parameters):
    print('Vissim Simulation will now Start')
    for i in range(0, simulation_parameters[0],simulation_parameters[1] ):
        Vissim.Simulation.RunSingleStep()
        Veh_C2X_attributes = Vissim.Net.Vehicles.GetMultipleAttributes(('VehType', 'No'))
        for cnt_C2X_veh in range(len(Veh_C2X_attributes)):
           print( Veh_C2X_attributes[cnt_C2X_veh][1])
    print('Vissim Simulation is now Complete')