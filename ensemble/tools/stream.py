""" 
    This module handles the Simulation response converting it into proper formats for querying data afterwards. 
"""


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class DataQuery:
    def __init__(self):
        self._str_response = ""
        self._vehs = []

    def __repr__(self):
        return f"{self.__class__.__name__}()"
