""" 
    This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""




# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class DataQuery:
    def __init__(self, channels):
        # maps event names to subscribers
        # str -> dict
        self.channels = {channel: dict() for channel in channels}
        self._str_response = ""
        self._vehs = []

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def get_subscribers(self, channel):
        return self.channels[channel]

    def register(self, channel, who, callback=None):
        if callback == None:
            callback = getattr(who, "update")
        self.get_subscribers(channel)[who] = callback

    def unregister(self, channel, who):
        del self.get_subscribers(channel)[who]

    def dispatch(self, channel, message):
        for subscriber, callback in self.get_subscribers(channel).items():
            callback(message)
