"""
Auxiliary geometry
==================
"""


# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import numpy as np
from dataclasses import dataclass
from functools import cached_property

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class Point:
    x: float
    y: float

    @cached_property
    def vect(self):
        """Colection"""
        return np.asarray((self.x, self.y))

    def norm(self):
        """Norm"""
        return np.linalg.norm(self.vect)

    def mean(self):
        """Mean"""
        return np.asarray(self.vect).mean()

    def distanceto(self, point):
        """Distance to other"""
        return np.linalg.norm(point.vect - self.vect)

    def findperpendicular(self):
        """Find a perpendicular vector"""
        try:
            ac_wise = (
                np.array([-self.y / self.x, 1])
                if self.x > 0
                else np.array([self.y / self.x, -1])
            )
            return Point(ac_wise[0], ac_wise[1])
        except ZeroDivisionError:
            c_wise = (
                np.array([1, -self.x / self.y])
                if self.y > 0
                else np.array([-1, self.x / self.y])
            )
            return Point(-c_wise[0], -c_wise[1])

    def isbehindof(self, m):
        """Returns true if point infront this one"""
        # Based on https://stackoverflow.com/questions/1560492/how-to-tell-whether-a-point-is-to-the-right-or-left-side-of-a-line
        # A : acwise vector,  B: origin, M: point
        # sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
        n = self.findperpendicular()
        a = n + self
        b = self
        return (
            np.sign((b.x - a.x) * (m.y - a.y) - (b.y - a.y) * (m.x - a.x)) > 0
        )

    def isinfrontof(self, m):
        """Returns true if point behind of this one"""
        n = self.findperpendicular()
        a = n + self
        b = self
        return (
            np.sign((b.x - a.x) * (m.y - a.y) - (b.y - a.y) * (m.x - a.x)) < 0
        )

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)


if __name__ == "__main__":
    a = Point(1, 1)
    b = Point(3, 3)
    print(
        f"""
        This is: {repr(a)},
        norm of: {a.norm()},
        mean of: {a.mean()},
        this is: {repr(b)},
        distance from {repr(a)} to {repr(b)}: {a.distanceto(b)},
        Anti clockwise vector to {repr(a)}: {a.findperpendicular()},
        Is {repr(a)} in front of {repr(b)}: {a.isinfrontof(b)},
        Is {repr(a)} behind of {repr(b)}: {a.isbehindof(b)},
        """
    )
