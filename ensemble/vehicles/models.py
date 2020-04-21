"""
    This submodule contains objects describing vehicles type and vehicle information. 
"""

import itertools


class Vehicle(object):
    """ Class defining a generic vehicle either from SymuVia or Vissim 

        When declaring the object for first time: 

        * :param abscissa: Initial x coordinate of the vehicle  [m]
        * :param acceleration: Initial condition for acceleration [m/s2]
        * :param distance: Initial travelled distance [m]
        * :param vehid: Vehicle id retrived from simulator [int]
        * :param ordinate: Initial y coordinate of the vehicle [m]
        * :param link: Initial name of the link [str]
        * :param vehtype: Vehicle type [str]
        * :param speed: Initial vehicle speed [m/s]
        * :param lane: Initial lane [int]
        * :param elevation: vehicle elevation [m]
        * :param dynamic: vehicle dynamic [fun]
        * :param itinerary: trip path [list]
        * :param max_speed: speed limit [m/s]
        * :param shw_speed: shockwave speed [m/s]
        * :param max_density: maximum density [veh/m]
    """

    counter = itertools.count()

    def __init__(
        self,
        abscissa=0.0,
        acceleration=0.0,
        distance=0.0,
        vehid=0,
        ordinate=0.0,
        link="",
        vehtype="",
        speed=0.0,
        lane=0,
        elevation=0.0,
        dynamic=None,
        itinerary=None,
        ff_speed=None,
        swh_speed=None,
        jam_density=None,
    ):
        """  Vehicle data container 

            :param abscissa: x coordinate of the vehicle [m], defaults to 0.0
            :type abscissa: float, optional
            :param acceleration: acceleration [m/s2], defaults to 0.0
            :type acceleration: float, optional
            :param distance: travelled distance [m], defaults to 0.0
            :type distance: float, optional
            :param vehid: behicle id retrived from simulator [int], defaults to 0
            :type vehid: int, optional
            :param ordinate: y coordinate of the vehicle [m], defaults to 0.0
            :type ordinate: float, optional
            :param link: name of the link [str], defaults to ""
            :type link: str, optional
            :param vehtype: ehicle type [str], defaults to ""
            :type vehtype: str, optional
            :param speed: vehicle speed [m/s], defaults to 0.0
            :type speed: float, optional
            :param lane: initial lane [int], defaults to 0
            :type lane: int, optional
            :param elevation: vehicle elevation [m], defaults to 0.0
            :type elevation: float, optional
            :param dynamic: vehicle dynamic , defaults to None
            :type dynamic: [type], optional
            :param itinerary: [description], defaults to None
            :type itinerary: [type], optional
        """
        self.abscissa = abscissa
        self.acceleration = acceleration
        self.distance = distance
        self.vehid = vehid
        self.ordinate = ordinate
        self.link = link
        self.vehtype = vehtype
        self.speed = speed
        self.lane = lane
        self.elevation = elevation
        self.dynamic = dynamic
        self.itinerary = itinerary

    def __repr__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"

    def __str__(self):
        data_dct = ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({data_dct})"
    def leader(self):
        leader=Vehicle(self.id)
        return leader
    def is_platoon_vehicle(self):
        if self.vehtype=='ensembletruck':
         return True