"""
Symuvia XML Parser
==================
A parser for trajectories from symuvia. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================
import re
from functools import cached_property

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.tools.constants import FIELD_FORMAT, FIELD_DATA

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


PATTERN = {
    "abs": re.compile(r'abs="(.*?)"'),
    "acc": re.compile(r'acc="(.*?)"'),
    "dst": re.compile(r'dst="(.*?)"'),
    "etat_pilotage": re.compile(
        r'dst="([\d\.]*?)"( etat_pilotage=".*?")? id="(.*?)"'
    ),
    "id": re.compile(
        r'dst="([\d\.]*?)"( etat_pilotage=".*?")? id="(.*?)" ord="(.*?)"'
    ),
    "ord": re.compile(r'ord="(.*?)"'),
    "tron": re.compile(r'tron="(.*?)"'),
    "type": re.compile(r'tron="(.*?)" type="(.*?)" vit="(.*?)"'),
    "vit": re.compile(r'vit="(.*?)"'),
    "voie": re.compile(r'voie="(.*?)"'),
    "z": re.compile(r'z="(.*?)"'),
    "traj": re.compile(
        r'abs="(.*?)" acc="(.*?)" dst="([\d\.]*?)"( etat_pilotage=".*?")? id="(.*?)" ord="(.*?)" tron="(.*?)" type="(.*?)" vit="(.*?)" voie="(.*?)" z="(.*?)"'
    ),
    "inst": re.compile(r'val="(.*?)"'),
    "nbveh": re.compile(r'nbVeh="(.*?)"'),
}

CAV_TYPE = tuple(value for key, value in FIELD_FORMAT.items())


class XMLTrajectory:
    """Model object for a trajectory, it can be created from a xml and contains trajectories for a set of vehicles."""

    aliases = {
        "abscissa": "abs",
        "acceleration": "acc",
        "distance": "dst",
        "elevation": "z",
        "lane": "voie",
        "link": "tron",
        "ordinate": "ord",
        "speed": "vit",
        "vehid": "id",
        "vehtype": "type",
    }

    def __init__(self, xml: bytes):
        self._xml = xml.decode("UTF8")

    def __getattr__(self, name):
        if name == "aliases":
            raise AttributeError  # http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)

    @cached_property
    def abs(self) -> tuple:
        """`abs` cached values for all vehicles in network

        Returns:
            tuple: cached `abs` values
        """
        return tuple(
            map(
                FIELD_FORMAT["abs"],
                PATTERN.get("abs").findall(self._xml),
            )
        )

    @cached_property
    def acc(self):
        """`acceleration` cached values for all vehicles in network

        Returns:
            tuple: cached `acc` values
        """
        return tuple(
            map(FIELD_FORMAT["acc"], PATTERN.get("acc").findall(self._xml))
        )

    @cached_property
    def dst(self):
        """`distance` cached values for all vehicles in network

        Returns:
            tuple: cached `dst` values
        """
        return tuple(
            map(FIELD_FORMAT["dst"], PATTERN.get("dst").findall(self._xml))
        )

    @cached_property
    def driven(self):
        """alias for `etat_pilotage`"""
        return self.etat_pilotage

    @cached_property
    def etat_pilotage(self):
        """`etat_pilotage` cached values for all vehicles in network

        Returns:
            tuple: cached `etat_pilotage` values
        """
        drv = PATTERN.get("etat_pilotage").findall(self._xml)
        if drv:
            return tuple(
                map(FIELD_FORMAT["etat_pilotage"], [x[1] for x in drv])
            )

    @cached_property
    def id(self):
        """Vehicle `id` cached values for all vehicles in network

        Returns:
            tuple: cached `id` values
        """
        return tuple(
            map(
                FIELD_FORMAT["id"],
                [x[-2] for x in PATTERN.get("id").findall(self._xml)],
            )
        )

    @cached_property
    def ord(self):
        """`ordinate` cached values for all vehicles in network

        Returns:
            tuple: cached `ord` values
        """
        return tuple(
            map(FIELD_FORMAT["ord"], PATTERN.get("ord").findall(self._xml))
        )

    @cached_property
    def tron(self):
        """`link` cached values for all vehicles in network

        Returns:
            tuple: cached `tron` values
        """
        return tuple(PATTERN.get("tron").findall(self._xml))

    @cached_property
    def type(self):
        """Vehicle `type` cached values for all vehicles in network

        Returns:
            tuple: cached `type` values
        """
        return tuple(x[1] for x in PATTERN.get("type").findall(self._xml))

    @cached_property
    def vit(self):
        """`speed` cached values for all vehicles in network

        Returns:
            tuple: cached `vit` values
        """
        return tuple(
            map(FIELD_FORMAT["vit"], PATTERN.get("vit").findall(self._xml))
        )

    @cached_property
    def voie(self):
        """`lane` cached values for all vehicles in network

        Returns:
            tuple: cached `voie` values
        """
        return tuple(
            map(FIELD_FORMAT["voie"], PATTERN.get("voie").findall(self._xml))
        )

    @cached_property
    def z(self):
        """`elevation` cached values for all vehicles in network

        Returns:
            tuple: cached `z` values
        """
        return tuple(map(float, PATTERN.get("z").findall(self._xml)))

    @cached_property
    def traj(self):
        """Trajectory cached values for all vehicles in network

        Returns:
            tuple: cached `traj` values
        """
        return tuple(
            XMLTrajectory._typeconvert(x)
            for x in PATTERN.get("traj").findall(self._xml)
        )

    @cached_property
    def inst(self):
        """`val` simulation time instant for current trajectory

        Returns:
            float: simulation time
        """
        return float(PATTERN.get("inst").findall(self._xml)[0])

    @cached_property
    def nbveh(self):
        """`nbveh` simulation time instant for current trajectory

        Returns:
            int: number of vehicles
        """
        return int(PATTERN.get("nbveh").findall(self._xml)[0])

    @cached_property
    def todict(self):
        """Converts to dictionary any of the data in the"""
        # Relies on order
        return tuple(dict(zip(FIELD_DATA.values(), x)) for x in self.traj)

    @classmethod
    def _typeconvert(cls, data: tuple):
        return tuple(a(b) for a, b in zip(CAV_TYPE, data))
