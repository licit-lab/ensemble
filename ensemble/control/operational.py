"""
    This module contains objects that implement the operational control layer or medium to communicate with other strategies
"""


class OperationalControl(object):
    """
        Operational Control     
    """

    def __init__(self):
        self.op_library = None
        self._kv = 0.5
        self._ks = 0.5

    def __call__(self, speed, hwy_x=None):
        return self.compute_control(speed, hwy_x)

    def compute_control(self, speed, hwy_x):
        if self.op_library:
            return self.op_library.call_control(speed, hwy_x)
        return 0

    def register_control(self, control_func):
        self.op_library = control_func
