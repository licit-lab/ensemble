"""
    unit test for symupy.handler.symuvia.stream
    unit test for symupy.handler.vissim.stream    
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest
from xmltodict import parse
from ctypes import create_string_buffer

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.handler.symuvia.stream import SimulatorRequest as SymuviaRequest
from ensemble.handler.vissim.stream import SimulatorRequest as Vissimrequest
from ensemble.tools.constants import BUFFER_STRING

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def no_trajectory_xml():
    """ Emulates  a XML response for no trajectory case """
    STREAM = b'<INST nbVeh="0" val="1.00"><CREATIONS><CREATION entree="Ext_In" id="0" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS/><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def one_vehicle_xml():
    """ Emulates a XML response for 1 vehicle trajectory"""
    STREAM = b'<INST nbVeh="1" val="2.00"><CREATIONS><CREATION entree="Ext_In" id="1" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="25.00" acc="0.00" dst="25.00" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def two_vehicle_xml():
    """ Emulates  a XML response for 2 vehicle trajectories"""
    STREAM = b'<INST nbVeh="2" val="4.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="75.00" acc="0.00" dst="75.00" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="44.12" acc="0.00" dst="44.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def one_vehicle_forced_xml():
    """ Emulates a XML response for 1 vehicle forced trajectory"""
    STREAM = b'<INST nbVeh="1" val="3.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="48.00" acc="-2.00" dst="48.00" etat_pilotage="force (ecoulement respecte)" id="0" ord="0.00" tron="Zone_001" type="VL" vit="23.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def two_vehicle_one_forced_xml():
    """ Emulates a XML response for 1 vehicle forced amont 2 trajectories"""
    STREAM = b'<INST nbVeh="1" val="3.00"><CREATIONS><CREATION entree="Ext_In" id="2" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="50.00" acc="0.00" dst="50.00" etat_pilotage="force (ecoulement respecte)" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="19.12" acc="0.00" dst="19.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def three_vehicle_xml():
    """ Emulate a XML response for 3 vehicle trajectories"""
    STREAM = b'<INST nbVeh="3" val="6.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="125.00" acc="0.00" dst="125.00" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="94.12" acc="0.00" dst="94.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="50.00" acc="0.00" dst="50.00" id="2" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def no_trajectory_dct(no_trajectory_xml):
    """ Dictionary expected answer """
    return parse(no_trajectory_xml)


@pytest.fixture
def one_vehicle_dct(one_vehicle_xml):
    """ Dictionary expected answer """
    return parse(one_vehicle_xml)


@pytest.fixture
def two_vehicle_dct(two_vehicle_xml):
    """ Dictionary expected answer """
    return parse(two_vehicle_xml)


@pytest.fixture
def no_trajectory_vehicle_data():
    """ No trajectory vehicle data """
    return []


@pytest.fixture
def one_trajectory_vehicle_data():
    """ One trajectory vehicle data """
    return [
        {
            "abscissa": 25.0,
            "acceleration": 0.0,
            "distance": 25.0,
            "driven": False,
            "elevation": 0.0,
            "lane": 1,
            "link": "Zone_001",
            "ordinate": 0.0,
            "speed": 25.0,
            "vehid": 0,
            "vehtype": "VL",
        }
    ]


@pytest.fixture
def two_trajectory_vehicle_data():
    """ Two trajectory vehicle data """
    return [
        {
            "abscissa": 75.0,
            "acceleration": 0.0,
            "distance": 75.0,
            "driven": False,
            "elevation": 0.0,
            "lane": 1,
            "link": "Zone_001",
            "ordinate": 0.0,
            "speed": 25.0,
            "vehid": 0,
            "vehtype": "VL",
        },
        {
            "abscissa": 44.12,
            "acceleration": 0.0,
            "distance": 44.12,
            "driven": False,
            "elevation": 0.0,
            "lane": 1,
            "link": "Zone_001",
            "ordinate": 0.0,
            "speed": 25.0,
            "vehid": 1,
            "vehtype": "VL",
        },
    ]


@pytest.fixture
def symuviarequest():
    return SymuviaRequest()


def test_constructor_request(symuviarequest):
    assert (
        symuviarequest.query.value == create_string_buffer(BUFFER_STRING).value
    )


def test_parse_nodata(symuviarequest):
    response = symuviarequest.data_query
    assert response == {}


def test_parse_notrajectory(
    symuviarequest, no_trajectory_xml, no_trajectory_dct
):
    symuviarequest.query = no_trajectory_xml
    response = symuviarequest.data_query
    assert response == no_trajectory_dct


def test_parse_1_vehicle(symuviarequest, one_vehicle_xml, one_vehicle_dct):
    symuviarequest.query = one_vehicle_xml
    response = symuviarequest.data_query
    assert response == one_vehicle_dct


def test_parse_2_vehicle(symuviarequest, two_vehicle_xml, two_vehicle_dct):
    symuviarequest.query = two_vehicle_xml
    response = symuviarequest.data_query
    assert response == two_vehicle_dct


def test_parse_notrajectory_vehicle_data(
    symuviarequest, no_trajectory_xml, no_trajectory_vehicle_data
):
    symuviarequest.query = no_trajectory_xml
    veh_data = symuviarequest.get_vehicle_data()
    assert veh_data == no_trajectory_vehicle_data


def test_parse_1_vehicle_data(
    symuviarequest, one_vehicle_xml, one_trajectory_vehicle_data
):
    symuviarequest.query = one_vehicle_xml
    veh_data = symuviarequest.get_vehicle_data()
    assert veh_data == one_trajectory_vehicle_data


def test_parse_2_vehicle_data(
    symuviarequest, two_vehicle_xml, two_trajectory_vehicle_data
):
    symuviarequest.query = two_vehicle_xml
    veh_data = symuviarequest.get_vehicle_data()
    assert veh_data == two_trajectory_vehicle_data


def test_parse_notrajectory_vehicle_property(symuviarequest, no_trajectory_xml):
    symuviarequest.query = no_trajectory_xml
    veh_data = symuviarequest.get_vehicles_property("vehtype")
    assert veh_data == tuple()
    veh_data = symuviarequest.get_vehicles_property("vehid")
    assert veh_data == tuple()
    veh_data = symuviarequest.get_vehicles_property("id")  # unexistent
    assert veh_data == tuple()


def test_parse_1_vehicle_property(symuviarequest, one_vehicle_xml):
    symuviarequest.query = one_vehicle_xml
    veh_data = symuviarequest.get_vehicles_property("vehtype")
    assert veh_data == ("VL",)
    veh_data = symuviarequest.get_vehicles_property("vehid")
    assert veh_data == (0,)
    veh_data = symuviarequest.get_vehicles_property("id")  # unexistent
    assert veh_data == (None,)


def test_parse_2_vehicle_data_property(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml
    veh_data = symuviarequest.get_vehicles_property("vehtype")
    assert veh_data == ("VL", "VL")
    veh_data = symuviarequest.get_vehicles_property("vehid")
    assert veh_data == (0, 1)
    veh_data = symuviarequest.get_vehicles_property("id")  # unexistent property
    assert veh_data == (None, None)


def test_parse_notrajectory_filter_property(symuviarequest, no_trajectory_xml):
    symuviarequest.query = no_trajectory_xml
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 0)
    assert veh_data == tuple()


def test_parse_1_vehicle_filter_property(symuviarequest, one_vehicle_xml):
    symuviarequest.query = one_vehicle_xml
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 0)
    assert veh_data == ("VL",)
    veh_data = symuviarequest.filter_vehicle_property("vehid", 0)
    assert veh_data == (0,)
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 0
    )  # unexistent property
    assert veh_data == (None,)

    # Unexisting vehicle
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 1)
    assert veh_data == tuple()
    veh_data = symuviarequest.filter_vehicle_property("vehid", 1)
    assert veh_data == tuple()
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 1
    )  # unexistent property
    assert veh_data == tuple()

    # Multiple vehicles
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 0, 1)
    assert veh_data == ("VL",)
    veh_data = symuviarequest.filter_vehicle_property("vehid", 0, 1)
    assert veh_data == (0,)
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 0, 1
    )  # unexistent property
    assert veh_data == (None,)


def test_parse_2_vehicle_filter_property(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 0)
    assert veh_data == ("VL",)
    veh_data = symuviarequest.filter_vehicle_property("vehid", 0)
    assert veh_data == (0,)
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 0
    )  # unexistent property
    assert veh_data == (None,)

    # Unexisting vehicle
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 1)
    assert veh_data == ("VL",)
    veh_data = symuviarequest.filter_vehicle_property("vehid", 1)
    assert veh_data == (1,)
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 1
    )  # unexistent property
    assert veh_data == (None,)

    # Multiple vehicles
    veh_data = symuviarequest.filter_vehicle_property("vehtype", 0, 1)
    assert veh_data == ("VL", "VL")
    veh_data = symuviarequest.filter_vehicle_property("vehid", 0, 1)
    assert veh_data == (0, 1)
    veh_data = symuviarequest.filter_vehicle_property(
        "id", 0, 1
    )  # unexistent property
    assert veh_data == (None, None)


def test_parse_notrajectory_is_vehicle(symuviarequest, no_trajectory_xml):
    symuviarequest.query = no_trajectory_xml
    b0 = symuviarequest.is_vehicle_in_network(0)
    assert b0 == False

    b01 = symuviarequest.is_vehicle_in_network(0, 1)
    assert b01 == False


def test_parse_1_vehicle_is_vehicle(symuviarequest, one_vehicle_xml):
    symuviarequest.query = one_vehicle_xml

    b0 = symuviarequest.is_vehicle_in_network(0)
    assert b0 == True

    b01 = symuviarequest.is_vehicle_in_network(0, 1)
    assert b01 == False


def test_parse_2_vehicle_is_vehicle(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml

    b0 = symuviarequest.is_vehicle_in_network(0)
    assert b0 == True

    b01 = symuviarequest.is_vehicle_in_network(0, 1)
    assert b01 == True


def test_parse_notrajectory_vehicles_in_link(symuviarequest, no_trajectory_xml):
    symuviarequest.query = no_trajectory_xml
    vehids = symuviarequest.vehicles_in_link("Zone_001")
    assert vehids == tuple()

    vehids = symuviarequest.vehicles_in_link("Zone_001", 2)
    assert vehids == tuple()


def test_parse_1_vehicle_vehicles_in_link(symuviarequest, one_vehicle_xml):
    symuviarequest.query = one_vehicle_xml
    vehids = symuviarequest.vehicles_in_link("Zone_001")
    assert vehids == (0,)

    vehids = symuviarequest.vehicles_in_link("Zone_001", 2)
    assert vehids == tuple()


def test_parse_2_vehicle_vehicles_in_link(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml
    vehids = symuviarequest.vehicles_in_link("Zone_001")
    assert vehids == (0, 1)

    vehids = symuviarequest.vehicles_in_link("Zone_001", 2)
    assert vehids == tuple()


def test_parse_notrajectory_is_vehicles_in_link(
    symuviarequest, no_trajectory_xml
):
    symuviarequest.query = no_trajectory_xml
    b0 = symuviarequest.is_vehicle_in_link(0, "Zone_001")
    assert b0 == False

    b01 = symuviarequest.is_vehicle_in_link(1, "Zone_001")
    assert b01 == False


def test_parse_1_vehicle_is_vehicle_in_link(symuviarequest, one_vehicle_xml):
    symuviarequest.query = one_vehicle_xml

    b0 = symuviarequest.is_vehicle_in_link(0, "Zone_001")
    assert b0 == True

    b01 = symuviarequest.is_vehicle_in_link(1, "Zone_001")
    assert b01 == False


def test_parse_2_vehicle_is_vehicle_in_link(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml

    b0 = symuviarequest.is_vehicle_in_link(0, "Zone_001")
    assert b0 == True

    b01 = symuviarequest.is_vehicle_in_link(1, "Zone_001")
    assert b01 == True


def test_parse_1_vehicle_is_vehicle_driven(
    symuviarequest, one_vehicle_forced_xml
):
    symuviarequest.query = one_vehicle_forced_xml

    b0 = symuviarequest.is_vehicle_driven(0)
    assert b0 == True


def test_parse_2_vehicle_is_vehicle_driven(symuviarequest, two_vehicle_xml):
    symuviarequest.query = two_vehicle_xml

    b0 = symuviarequest.is_vehicle_driven(0)
    assert b0 == False


def test_parse_2_vehicle_downstream_of(symuviarequest, three_vehicle_xml):
    symuviarequest.query = three_vehicle_xml

    b0 = symuviarequest.vehicle_downstream_of(2)
    assert b0 == (0, 1)

    b0 = symuviarequest.vehicle_downstream_of(1)
    assert b0 == (0,)

    b0 = symuviarequest.vehicle_downstream_of(0)
    assert b0 == tuple()


def test_parse_2_vehicle_upstream_of(symuviarequest, three_vehicle_xml):
    symuviarequest.query = three_vehicle_xml

    b0 = symuviarequest.vehicle_upstream_of(0)
    assert b0 == (1, 2)

    b0 = symuviarequest.vehicle_upstream_of(1)
    assert b0 == (2,)

    b0 = symuviarequest.vehicle_upstream_of(2)
    assert b0 == tuple()


def test_parse_3_get_vehicle_properties(
    symuviarequest, three_vehicle_xml, one_trajectory_vehicle_data
):
    symuviarequest.query = three_vehicle_xml

    b0 = symuviarequest.get_vehicle_properties(0)
    b1 = symuviarequest.get_vehicle_properties(1)
    assert set(b0.keys()) == set(one_trajectory_vehicle_data[0].keys())
    assert set(b1.keys()) == set(one_trajectory_vehicle_data[0].keys())


def test_parse_2_get_vehicle_properties(
    symuviarequest, two_vehicle_one_forced_xml, one_trajectory_vehicle_data
):
    symuviarequest.query = two_vehicle_one_forced_xml

    b0 = symuviarequest.get_vehicle_properties(0)
    b1 = symuviarequest.get_vehicle_properties(1)
    assert set(b0.keys()) == set(one_trajectory_vehicle_data[0].keys())
    assert set(b1.keys()) == set(one_trajectory_vehicle_data[0].keys())


def test_retrieve_time_step(symuviarequest, three_vehicle_xml):
    symuviarequest.query = three_vehicle_xml
    assert symuviarequest.current_time == 6.00


def test_retrieve_nb_veh(symuviarequest, three_vehicle_xml):
    symuviarequest.query = three_vehicle_xml
    assert symuviarequest.current_nbveh == 3
