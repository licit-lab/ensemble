"""
    Unit testing Tactical Layer (Front Gap)
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform
import pytest
from collections import namedtuple
from jinja2 import Environment, PackageLoader, select_autoescape
from ctypes import create_string_buffer

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.handler.symuvia.stream import SimulatorRequest as SymuviaRequest
from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Cutin,
    Splitting,
)

from ensemble.component.vehiclelist import VehicleList
from ensemble.control.tactical.gapcordinator import GlobalGapCoordinator

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

# Testing Data


@pytest.fixture
def TEST01():
    """StandAlone -> Join
    No PCM Capable
    """
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


@pytest.fixture
def TEST02():
    """StandAlone -> Join
    Far Away
    """
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
            True,
            True,
        )
        for i in range(1, 3)
    ]


@pytest.fixture
def TEST03():
    """StandAlone -> Join
    Truck 7 not Joinable
    """
    case = [
        trkdata(
            0,
            0,
            435 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            435 - (30 * 1.4 + 3) * i,
            30,
            i,
            "PLT",
            StandAlone(),
            True,
            True,
        )
        for i in range(1, 8)
    ]

    case.append(
        trkdata(
            0,
            0,
            80,
            False,
            0,
            1,
            "LinkA",
            80,
            20,
            8,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST04():
    """StandAlone -> Join"""
    case = [
        trkdata(
            0,
            0,
            480 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            480 - (30 * 1.4 + 3) * i,
            30,
            i,
            "PLT",
            StandAlone(),
            True,
            True,
        )
        for i in range(1, 5)
    ]

    case = case + [
        trkdata(
            0,
            0,
            445 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            445 - (30 * 1.4 + 3) * i,
            20,
            i,
            "PLT",
            StandAlone(),
            True,
            True,
        )
        for i in range(5, 8)
    ]
    return case


@pytest.fixture
def TEST05():
    """StandAlone -> Join"""
    case = [
        trkdata(
            0,
            0,
            480 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            480 - (30 * 1.4 + 3) * i,
            30,
            i,
            "PLT",
            StandAlone(),
            True,
            True,
        )
        for i in range(1, 5)
    ]

    case = case + [
        trkdata(
            0,
            0,
            445 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            445 - (30 * 1.4 + 3) * i,
            20,
            i,
            "PLT",
            StandAlone(),
            True,
            True,
        )
        for i in range(5, 7)
    ]
    return case


@pytest.fixture
def TEST06():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        ),
    ]

    case.append(
        (
            0,
            0,
            200,
            False,
            0,
            2,
            "LinkA",
            200,
            30,
            1,
            "HDV",
        )
    )

    case.append(
        trkdata(
            0,
            0,
            80,
            False,
            0,
            3,
            "LinkA",
            80,
            20,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST07():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            20,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        ),
    ]

    case.append(
        trkdata(
            0,
            0,
            90,
            False,
            0,
            1,
            "LinkA",
            90,
            20,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST08():
    case = [
        trkdata(
            0,
            0,
            245 - (30 * 1.4 + 3) * i,
            False,
            0,
            1,
            "LinkA",
            245 - (30 * 1.4 + 3) * i,
            30,
            i,
            "PLT",
            StandAlone(),
            True,
            False,
        )
        for i in range(1, 2)
    ]

    case.append(
        trkdata(
            0,
            0,
            120,
            False,
            0,
            1,
            "LinkA",
            120,
            20,
            2,
            "PLT",
            Joining(),
            True,
            False,
        )
    )
    return case


@pytest.fixture
def TEST09():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            False,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            120,
            False,
            0,
            1,
            "LinkA",
            120,
            20,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )

    return case


@pytest.fixture
def TEST10():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            120,
            False,
            0,
            1,
            "LinkA",
            120,
            20,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST11():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            153,
            False,
            0,
            1,
            "LinkA",
            153,
            30,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST12():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            156.5,
            False,
            0,
            1,
            "LinkA",
            156.5,
            28.9,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST13():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            154.92,
            False,
            0,
            1,
            "LinkA",
            154.92,
            29.99,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST14():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            False,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            155,
            False,
            0,
            1,
            "LinkA",
            155,
            30,
            2,
            "PLT",
            Joining(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST15():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            155,
            False,
            0,
            1,
            "LinkA",
            155,
            30,
            2,
            "PLT",
            Joining(),
            False,
            True,
        )
    )
    return case


@pytest.fixture
def TEST16():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]
    case.append(
        trkdata(
            0,
            0,
            155,
            False,
            0,
            1,
            "LinkA",
            155,
            30,
            2,
            "PLT",
            Platooning(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST17():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        (
            0,
            0,
            200,
            False,
            0,
            2,
            "LinkA",
            155,
            30,
            1,
            "HDV",
        )
    )

    case.append(
        trkdata(
            0,
            0,
            137,
            False,
            0,
            1,
            "LinkA",
            137,
            30,
            3,
            "PLT",
            Platooning(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST18():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        (
            0,
            0,
            155,
            False,
            0,
            2,
            "LinkA",
            155,
            30,
            1,
            "HDV",
        )
    )

    case.append(
        trkdata(
            0,
            0,
            137,
            False,
            0,
            1,
            "LinkA",
            137,
            30,
            3,
            "PLT",
            Cutin(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST19():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        (
            0,
            0,
            155,
            False,
            0,
            2,
            "LinkA",
            155,
            30,
            1,
            "HDV",
        )
    )

    case.append(
        trkdata(
            0,
            0,
            137,
            False,
            0,
            1,
            "LinkA",
            137,
            30,
            3,
            "PLT",
            Cutin(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST20():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            137,
            False,
            0,
            1,
            "LinkA",
            137,
            30,
            3,
            "PLT",
            Cutin(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST21():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            137,
            False,
            0,
            1,
            "LinkA",
            137,
            30,
            3,
            "PLT",
            Splitting(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def TEST22():
    case = [
        trkdata(
            0,
            0,
            200,
            False,
            0,
            1,
            "LinkA",
            200,
            30,
            1,
            "PLT",
            StandAlone(),
            True,
            True,
        )
    ]

    case.append(
        trkdata(
            0,
            0,
            140,
            False,
            0,
            1,
            "LinkA",
            140,
            30,
            3,
            "PLT",
            Splitting(),
            True,
            True,
        )
    )
    return case


@pytest.fixture
def symuviarequest():
    return SymuviaRequest()


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
    return bytes(template.render(vehicles=VEHICLES), encoding="UTF8")


# ============================================================================
# TESTS
# ============================================================================


def test_01_standalone_to_join_no_PCM_available(
    symuviarequest: SymuviaRequest, TEST01: list
):
    symuviarequest.query = transform_data(TEST01)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert isinstance(ggc[1].status, StandAlone)
    assert isinstance(ggc[2].status, StandAlone)


def test_02_standalone_to_join_far_away(
    symuviarequest: SymuviaRequest, TEST02: list
):
    symuviarequest.query = transform_data(TEST02)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert isinstance(ggc[1].status, StandAlone)
    assert isinstance(ggc[2].status, StandAlone)


def test_03_standalone_to_join(symuviarequest: SymuviaRequest, TEST03: list):
    symuviarequest.query = transform_data(TEST03)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_04_(symuviarequest: SymuviaRequest, TEST04: list):
    symuviarequest.query = transform_data(TEST04)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_05_(symuviarequest: SymuviaRequest, TEST05: list):
    symuviarequest.query = transform_data(TEST05)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_06_(symuviarequest: SymuviaRequest, TEST06: list):
    symuviarequest.query = transform_data(TEST06)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_07_(symuviarequest: SymuviaRequest, TEST07: list):
    symuviarequest.query = transform_data(TEST07)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_08_(symuviarequest: SymuviaRequest, TEST08: list):
    symuviarequest.query = transform_data(TEST08)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_09_(symuviarequest: SymuviaRequest, TEST09: list):
    symuviarequest.query = transform_data(TEST09)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_10_(symuviarequest: SymuviaRequest, TEST10: list):
    symuviarequest.query = transform_data(TEST10)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_11_(symuviarequest: SymuviaRequest, TEST11: list):
    symuviarequest.query = transform_data(TEST11)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_12_(symuviarequest: SymuviaRequest, TEST12: list):
    symuviarequest.query = transform_data(TEST12)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_13_(symuviarequest: SymuviaRequest, TEST13: list):
    symuviarequest.query = transform_data(TEST13)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_14_(symuviarequest: SymuviaRequest, TEST14: list):
    symuviarequest.query = transform_data(TEST14)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_15_(symuviarequest: SymuviaRequest, TEST15: list):
    symuviarequest.query = transform_data(TEST15)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_16_(symuviarequest: SymuviaRequest, TEST16: list):
    symuviarequest.query = transform_data(TEST16)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_17_(symuviarequest: SymuviaRequest, TEST17: list):
    symuviarequest.query = transform_data(TEST17)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_18_(symuviarequest: SymuviaRequest, TEST18: list):
    symuviarequest.query = transform_data(TEST18)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_19_(symuviarequest: SymuviaRequest, TEST19: list):
    symuviarequest.query = transform_data(TEST19)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_20_(symuviarequest: SymuviaRequest, TEST20: list):
    symuviarequest.query = transform_data(TEST20)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_21_(symuviarequest: SymuviaRequest, TEST21: list):
    symuviarequest.query = transform_data(TEST21)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


def test_22_(symuviarequest: SymuviaRequest, TEST22: list):
    symuviarequest.query = transform_data(TEST22)
    vehlist = VehicleList(symuviarequest)
    ggc = GlobalGapCoordinator(vehlist)
    ggc.update_platoons()
    assert True


# #
# # def test_2():
# #     veh=PlatoonVehicle(leader_PCM_capable=1,
# #     leader_split_request=False,
# #     ego_distance_gap_to_leader=0,
# #     leader_id=1,
# #     leader_speed=4.0,
# #     leader_length=5.0,
# #     gap_distance_error=0,
# #     ego_split_request=False,
# #     ego_standalone_time_gap=1,
# #     front_target_state="join",
# #     ego_speed=4.0,
# #     ego_position=0,
# #     leader_position=0,
# #     desired_gap=1,
# #     standalone_gap=1,
# #     platoon_id=1,
# #     platoon_length=1,
# #     front_id=2,
# #     intruder=False,
# #     ego_platoon_position=1,
# #     leader_platoon_position=2,
# #     maximum_platoon_length=7,
# #     platoon_desired_speed=50,
# #     platoon_desired_time_gap=2,
# #     max_connection_distance=100)
# #     fgc = FrontGapState( veh)
# #     fgc.update_state(veh)
# #     assert veh.front_target_state=="platoon"
# #
# # def test_3():
# #     veh=PlatoonVehicle(leader_PCM_capable=1,
# #     leader_split_request=False,
# #     ego_distance_gap_to_leader=0,
# #     leader_id=1,
# #     leader_speed=4.0,
# #     leader_length=5.0,
# #     gap_distance_error=0,
# #     ego_split_request=False,
# #     ego_standalone_time_gap=1,
# #     front_target_state="standalone",
# #     ego_speed=4.0,
# #     ego_position=0,
# #     leader_position=0,
# #     desired_gap=1,
# #     standalone_gap=1,
# #     platoon_id=1,
# #     platoon_length=1,
# #     front_id=2,
# #     intruder=False,
# #     ego_platoon_position=1,
# #     leader_platoon_position=2,
# #     maximum_platoon_length=7,
# #     platoon_desired_speed=50,
# #     platoon_desired_time_gap=2,
# #     max_connection_distance=100)
# #     fgc = FrontGapState( veh)
# #     fgc.update_state(veh)
# #     assert veh.front_target_state=="join"
# #
# # def test_4():
# #     veh=PlatoonVehicle(leader_PCM_capable=1,
# #     leader_split_request=False,
# #     ego_distance_gap_to_leader=0,
# #     leader_id=1,
# #     leader_speed=4.0,
# #     leader_length=5.0,
# #     gap_distance_error=0,
# #     ego_split_request=False,
# #     ego_standalone_time_gap=1,
# #     front_target_state="platoon",
# #     ego_speed=4.0,
# #     ego_position=0,
# #     leader_position=0,
# #     desired_gap=1,
# #     standalone_gap=1,
# #     platoon_id=1,
# #     platoon_length=1,
# #     front_id=2,
# #     intruder=True,
# #     ego_platoon_position=1,
# #     leader_platoon_position=2,
# #     maximum_platoon_length=7,
# #     platoon_desired_speed=50,
# #     platoon_desired_time_gap=2,
# #     max_connection_distance=100)
# #     fgc = FrontGapState( veh)
# #     fgc.update_state(veh)
# #     assert veh.front_target_state=="frontsplit"

# def test_1_standalone_to_join_no_PCM_available():
#     veh = PlatoonVehicle(
#     leader_id=101,
#     leader_length=0,
#     leader_position=200,
#     leader_speed=30,
#     leader_PCM_capable=	False,
#     leader_split_request=False,
#     leader_platoon_position	=1,
#     ego_position	=50,
#     ego_speed	=20,
#     ego_distance_gap_to_leader=150,
#     desired_gap	=31,
#     ego_standalone_time_gap=2,
#     standalone_gap	=43,
#     gap_distance_error	=119,
#     ego_split_request	=False,
#     front_target_state	="standalone",
#     platoon_id	=0,
#     platoon_length	=0,
#     front_id	=0,
#     intruder=False,
#     ego_platoon_position=	0,
#     maximum_platoon_length=	7,
#     platoon_desired_speed=	-99,
#     platoon_desired_time_gap=1.4,
#     max_connection_distance	=100)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"

# def test_2_standalone_to_join_far_away():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	1	,
#     ego_position	=	50	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	150	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	119	,
#     ego_split_request	=	False	,
#     front_target_state="standalone",
#     platoon_id	=	0	,
#     platoon_length	=	0	,
#     front_id	=	0	,
#     intruder=	False	,
#     ego_platoon_position	=	0	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_3_standalone_to_join_leader_not_joinable():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	7	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"standalone"	,
#     platoon_id	=	0	,
#     platoon_length	=	0	,
#     front_id	=	0	,
#     intruder=False	,
#     ego_platoon_position	=	0	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_4_standalone_to_join_success():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	5	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"standalone"	,
#     platoon_id	=	2001	,
#     platoon_length	=	2	,
#     front_id	=	0	,
#     intruder=False,
#     ego_platoon_position	=	1	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "join"

# def test_5_standalone_to_join_exceed_maximum_platoon_length():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	5	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"standalone"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	0	,
#     intruder=False	,
#     ego_platoon_position	=	1	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_6_join_to_standalone_intruder():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=True	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_7_join_to_standalone_leader_not_within_range():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	90	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	110	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	79	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=	False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"

# def test_8_join_to_standalone_leader_lost_PCM_connection():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	False	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_9_join_to_standalone_leader_is_leaving():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	True	,
#     leader_platoon_position	=	2	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False		,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_10_remain_join():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	120	,
#     ego_speed	=	20	,
#     ego_distance_gap_to_leader	=	80	,
#     desired_gap	=	31	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	43	,
#     gap_distance_error	=	49	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "join"
# def test_11_join_to_platoon_failed_1():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,#check with Lin
#     leader_platoon_position	=	2	,
#     ego_position	=	153	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	47	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	2	,
#     ego_split_request	=	False	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "join"
# def test_12_join_to_platoon_success_speed_error():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	156.5	,
#     ego_speed	=	28.90	,
#     ego_distance_gap_to_leader	=	43.5	,
#     desired_gap	=	43.46	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	60.8	,
#     gap_distance_error	=	0.04	,
#     ego_split_request	=	0	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "platoon"

# def test_13_join_to_platoon_success():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	154.92	,
#     ego_speed	=	29.99	,
#     ego_distance_gap_to_leader	=	45.08	,
#     desired_gap	=	44.986	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	62.98	,
#     gap_distance_error	=	0.094	,
#     ego_split_request	=	0	,
#     front_target_state	=	"join"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "platoon"
# def test_14_platooning_to_front_split_leader_wants_to_leave():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	True	,
#     leader_platoon_position	=	2	,
#     ego_position	=	155	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	45	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	False	,
#     front_target_state	=	"platoon"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "frontsplit"
# def test_15_platooning_to_front_split_ego_wants_to_leave():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	155	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	45	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	True	,
#     front_target_state	=	"platoon"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "frontsplit"
# def test_16_platooning_to_front_split():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	155	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	45	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	False	,
#     front_target_state	=	"platoon"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "platoon"
# def test_17_platooning_to_cutin_due_to_intruder():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	155	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	45	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	False	,
#     front_target_state	=	"platoon"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=True,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "cutin"

# def test_18_cutin_to_front_split():
#     veh = PlatoonVehicle(leader_id	=	999	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	137	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	63	,
#     desired_gap	=	63	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	False	,
#     front_target_state	=	"cutin",
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=True	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "frontsplit"
# def test_19_stay_cutin():
#     veh = PlatoonVehicle(leader_id	=	999	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	140	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	60	,
#     desired_gap	=	63	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	-3	,
#     ego_split_request	=	False	,
#     front_target_state	=	"cutin"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=True	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "cutin"
# def test_20_cutin_to_platoon():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	1	,
#     leader_split_request	=	0	,
#     leader_platoon_position	=	2	,
#     ego_position	=	140	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	60	,
#     desired_gap	=	45	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	15	,
#     ego_split_request	=	0	,
#     front_target_state	=	"cutin"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "platoon"
# def test_21_frontsplit_to_standalone():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	137	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	63	,
#     desired_gap	=	63	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	0	,
#     ego_split_request	=	False	,
#     front_target_state	=	"frontsplit"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "standalone"
# def test_22_stay_front_split():
#     veh = PlatoonVehicle(leader_id	=	101	,
#     leader_position	=	200	,
#     leader_speed	=	30	,
#     leader_PCM_capable	=	True	,
#     leader_split_request	=	False	,
#     leader_platoon_position	=	2	,
#     ego_position	=	140	,
#     ego_speed	=	30	,
#     ego_distance_gap_to_leader	=	60	,
#     desired_gap	=	63	,
#     ego_standalone_time_gap	=	2	,
#     standalone_gap	=	63	,
#     gap_distance_error	=	-3	,
#     ego_split_request	=	True	,
#     front_target_state	=	"frontsplit"	,
#     platoon_id	=	2001	,
#     platoon_length	=	3	,
#     front_id	=	101	,
#     intruder=False	,
#     ego_platoon_position	=	3	,
#     maximum_platoon_length	=	7	,
#     platoon_desired_speed	=	-99	,
#     platoon_desired_time_gap	=	1.4	,
#     max_connection_distance	=	100	)
#     fgc = FrontGapState(veh)
#     fgc.update_state(veh)
#     assert veh.front_target_state == "frontsplit"
