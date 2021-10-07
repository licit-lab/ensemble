"""
Platoon Set
===========
This is a class describing a frozen set. This is a collection implementation for a set of ordered elements that establish specific protocols for iteration, information access, element identification.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from collections.abc import Sequence, Set
from itertools import chain
from bisect import bisect_left
from itertools import count

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.logic.frozen_set import SortedFrozenSet
from ensemble.tools.constants import DCT_PLT_CONST


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

MAXTRKS = DCT_PLT_CONST["max_platoon_length"]
MAXNDST = DCT_PLT_CONST["max_connection_distance"]


class PlatoonSet(SortedFrozenSet):
    """
    This is a collection that provides a set of properties to create a platoon frozen set.

    In particular

    Args:
        Sequence (Sequence): Inherits from the `Sequence` collection object.
        Set (Set): Inherits from the `Set` collection object.
    """

    pid = count(0)

    def __init__(self, items=None, key="x", id: int = -1):
        self._items = tuple(
            sorted(
                set(items) if (items is not None) else set(),
                key=lambda x: getattr(x, key),
            )
        )
        self.platoonid = id if id >= 0 else next(self.__class__.pid)
        self.updatePids()

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        result = self._items[index]
        return PlatoonSet(result) if isinstance(index, slice) else result

    def __repr__(self):
        return "{type}-{id}({arg})".format(
            type=type(self).__name__,
            id=self.platoonid,
            arg=(
                "[{}]".format(", ".join(map(repr, self._items)))
                if self._items
                else ""
            ),
        )

    def __eq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self._items == rhs._items

    def __hash__(self):
        return hash((type(self), self._items))

    def __add__(self, rhs):

        if not isinstance(rhs, type(self)):
            return NotImplemented

        if len(self._items) + len(rhs._items) < MAXTRKS:
            # Join from the front
            if rhs.joinable():
                PlatoonSet.setPid(rhs.platoonid)
                return PlatoonSet(
                    tuple(chain(self._items, rhs._items)), id=self[-1].platoonid
                )

        return self, rhs

        # Join from the back

    def __mul__(self, rhs):
        return self if rhs > 0 else PlatoonSet()

    def __rmul__(self, lhs):
        return self * lhs

    def count(self, item):
        return int(item in self)

    def index(self, item):
        index = bisect_left(self._items, item)
        if (index != len(self._items)) and self._items[index] == item:
            return index
        raise ValueError(f"{item!r} not found")

    def issubset(self, iterable):
        return self <= PlatoonSet(iterable)

    def issuperset(self, iterable):
        return self >= PlatoonSet(iterable)

    def intersection(self, iterable):
        return self & PlatoonSet(iterable)

    def union(self, iterable):
        return self | PlatoonSet(iterable)

    def symmetric_difference(self, iterable):
        return self ^ PlatoonSet(iterable)

    def difference(self, iterable):
        return self - PlatoonSet(iterable)

    def joinable(self):
        """Exams last vehicle in the Platoon"""
        return self[-1].joinable

    def updatePids(self):
        """Exams and updates the Platoon Index Position"""
        for _, item in enumerate(self._items):
            item.platoonid = self.platoonid

    @classmethod
    def setPid(cls, value):
        """Set counter for the platoons"""
        cls.pid = count(value)
