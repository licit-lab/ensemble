"""
    This module provides functionalities for reading input parametrization for the platoon demand
"""

import pandas as pd


class DemandPlatoon(object):
    """ This object transforms csv requirements into car creation for vehicles within the traffic simulator
    """

    def __init__(self, file_name):
        self.demand_data = self.read_platoon_demand()

    def read_platoon_demand(file_name: str) -> pd.DataFrame:
        """ Read a csv file and returns a dataframe
        
        :param file_name: Path to file containing demand
        :type file_name: str
        :return: internal DataFrame to manage Platoon demand
        :rtype: pd.DataFrame
        """
        return pd.read_csv(file_name, sep=",")
