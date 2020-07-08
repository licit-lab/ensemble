""" 
    This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class DataQuery:
    """
        This general dataquery model implements a general publisher pattern to broadcast information towards different subscribers. Subscribers are intented to be objects such as vehicles, front/rear gap coordinators.
    """

    def __init__(self, channels):
        # maps event names to subscribers
        # str -> dict
        self.channels = {channel: dict() for channel in channels}
        self._str_response = ""
        self._vehs = []

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def get_subscribers(self, channel):
        """
            Retreive subscribers in a particular channel
        """
        return self.channels[channel]

    def register(self, channel:str, who, callback=None):
        """[summary]

            :param channel: Channel to register
            :type channel: str
            :param who: Type to register
            :type who: [type]
            :param callback: [description], defaults to None
            :type callback: [type], optional
        """
        if callback == None:
            callback = getattr(who, "update")
        self.get_subscribers(channel)[who] = callback

    def unregister(self, channel, who):
        del self.get_subscribers(channel)[who]

    def dispatch(self, channel, vehicle_env):
        for subscriber, callback in self.get_subscribers(channel).items():
            callback(vehicle_env)
