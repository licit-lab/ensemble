"""
    Unit testing for vehicle list
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from jinja2 import Environment, PackageLoader, select_autoescape
from collections import namedtuple
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.vehiclelist import VehicleList
from ensemble.handler.symuvia.stream import SimulatorRequest
from ensemble.logic.platoon_states import StandAlone

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================

KEYS = (
    "abscissa",
    "acceleration",
    "distance",
    "driven",
    "elevation",
    "lane",
    "link",
    "ordinate",
    "speed",
    "vehid",
    "vehtype",
    "status",
    "platoon",
    "comv2x",
)
trkdata = namedtuple("Truckdata", KEYS)

# ============================================================================
# GENERIC FUNCTIONS
# ============================================================================

env = Environment(
    loader=PackageLoader("ensemble", "templates"),
    autoescape=select_autoescape(
        [
            "xml",
        ]
    ),
)


def transform_data(TEST):
    VEHICLES = [dict(zip(KEYS, v)) for v in TEST]
    template = env.get_template("instant.xml")
    return str.encode(template.render(vehicles=VEHICLES), encoding="UTF8")


# ============================================================================
# TESTS
# ============================================================================


@pytest.fixture
def symuviarequest():
    return SimulatorRequest()


@pytest.fixture
def TEST01():
    return [
        trkdata(
            0,
            0,
            350 - 150 * i,
            False,
            0,
            1,
            "LinkA",
            350 - 150 * i,
            40 - i * 10,
            i,
            "PLT",
            StandAlone(),
            False,
            False,
        )
        for i in range(1, 3)
    ]


def test_get_leader(symuviarequest, TEST01):
    symuviarequest.query = transform_data(TEST01)
    vehlist = VehicleList(symuviarequest)
    assert vehlist.get_leader(vehlist[0]) is vehlist[0]
    assert vehlist.get_leader(vehlist[1]) is vehlist[1]


def test_get_leader_inrange(symuviarequest, TEST01):
    symuviarequest.query = transform_data(TEST01)
    vehlist = VehicleList(symuviarequest)
    assert vehlist.get_leader(vehlist[0], 200) is vehlist[0]
    assert vehlist.get_leader(vehlist[1], 200) is vehlist[0]


def test_get_follower(symuviarequest, TEST01):
    symuviarequest.query = transform_data(TEST01)
    vehlist = VehicleList(symuviarequest)
    assert vehlist.get_follower(vehlist[0]) is vehlist[0]
    assert vehlist.get_follower(vehlist[1]) is vehlist[1]


def test_get_follower_inrange(symuviarequest, TEST01):
    symuviarequest.query = transform_data(TEST01)
    vehlist = VehicleList(symuviarequest)
    assert vehlist.get_follower(vehlist[0], 200) is vehlist[1]
    assert vehlist.get_follower(vehlist[1], 200) is vehlist[1]
