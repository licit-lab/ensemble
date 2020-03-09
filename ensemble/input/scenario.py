"""
    Base class to operate with scenarios 
"""


class Scenario(object):
    """ 
        This class stores pointers towards important scenario files and methods to handle cross-simulated 
        functionalities 
    """

    def __init__(
        self, scn_file: str = None, layout_file: str = None, platoon_file: str = None,
    ):
        self.scn_file = scn_file
        self.layout_file = layout_file
        self.platoon_file = platoon_file

    def __repr__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"
