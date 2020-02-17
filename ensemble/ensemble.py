"""
    Main module to control 

"""

from .handler_vissim.vissim_functions import start_vissim_simulation,load_vissim_network,load_simulation_parameters

#from .handler_symuvia.new_file import my_func
#from .handler_vissim.start_vissim import another_function

# Config files


def launch_simulation():
    """ Launch Simulation """

    Vissim=start_vissim_simulation()
    load_vissim_network()
    load_simulation_parameters(Vissim)






def configure_scenario():
    """
    """
