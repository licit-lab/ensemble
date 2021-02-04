""" Unit Tests for `platoon frozen set` module"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================
import pytest
from collections.abc import Container, Sized, Iterable, Sequence, Hashable, Set

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.platoon import Platoon
from ensemble.handler.symuvia.stream import SimulatorRequest

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def six_vehicles():
    return b'<INST nbVeh="6" val="12.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="275.00" acc="0.00" dst="275.00" id="0" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="244.12" acc="0.00" dst="244.12" id="1" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="200.00" acc="0.00" dst="200.00" id="2" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="150.00" acc="0.00" dst="150.00" id="3" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="100.00" acc="0.00" dst="100.00" id="4" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="50.00" acc="0.00" dst="50.00" id="5" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'


@pytest.fixture
def seven_vehicles():
    return b'<INST nbVeh="7" val="16.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="375.00" acc="0.00" dst="375.00" id="0" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="344.12" acc="0.00" dst="344.12" id="1" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="300.00" acc="0.00" dst="300.00" id="2" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="250.00" acc="0.00" dst="250.00" id="3" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="200.00" acc="0.00" dst="200.00" id="4" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="150.00" acc="0.00" dst="150.00" id="5" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="100.00" acc="0.00" dst="100.00" id="6" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'


@pytest.fixture
def eight_vehicles():
    return b'<INST nbVeh="8" val="16.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="375.00" acc="0.00" dst="375.00" id="0" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="344.12" acc="0.00" dst="344.12" id="1" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="300.00" acc="0.00" dst="300.00" id="2" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="250.00" acc="0.00" dst="250.00" id="3" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="200.00" acc="0.00" dst="200.00" id="4" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="150.00" acc="0.00" dst="150.00" id="5" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="100.00" acc="0.00" dst="100.00" id="6" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="50.00" acc="0.00" dst="50.00" id="7" ord="0.00" tron="Zone_001" type="PL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'


@pytest.fixture
def simrequest():
    return SimulatorRequest()


def test_six_vehicle(simrequest, six_vehicles):
    simrequest.query = six_vehicles
    d = simrequest.get_vehicle_data()
    assert len(d) == 6


def test_seven_vehicle(simrequest, seven_vehicles):
    simrequest.query = seven_vehicles
    d = simrequest.get_vehicle_data()
    assert len(d) == 7


def test_eight_vehicle(simrequest, eight_vehicles):
    simrequest.query = eight_vehicles
    d = simrequest.get_vehicle_data()
    assert len(d) == 8


def test_create_platoon(simrequest, six_vehicles):
    simrequest.query == six_vehicles
    p = Platoon(simrequest)
    assert True
