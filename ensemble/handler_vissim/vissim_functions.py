import os
import json
import itertools
#import pandas as pd
import time
import win32com.client as com
import os
import numpy as np
def start_vissim_simulation():
    print('Hello Vissim SImulation  is Starting again')
    Vissim = com.gencache.EnsureDispatch("Vissim.Vissim-32.10")  # Vissim 10 - 64 bit
    GlosaNetworkPath = 'C:\\Users\\Public\\Documents\\GLOSA\\GlosaTrafficLight'
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.inpx')
    flag_read_additionally = False  # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(Filename, flag_read_additionally)
    ## Load a Layout:
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.layx')
    Vissim.LoadLayout(Filename)
    return Vissim
def load_vissim_network():
    print('Vissim Network is now Loaded')
    return
def load_simulation_parameters(Vissim):
    End_of_simulation = 600  # simulation second [s]
    Simulation_Resolution = 1  # simulation second [s]
    Number_Runs = 4
    Simulation_Period = 300
    Vissim.Simulation.SetAttValue('SimRes', Simulation_Resolution)
    Vissim.Simulation.SetAttValue('NumRuns', Number_Runs)
    Vissim.Simulation.SetAttValue('SimPeriod', Simulation_Period)
    print('Setup Complete')
    return