"""
    Unit testing Tactical Layer (Front Gap)
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from ensemble.component.platoon import Platoon
from ensemble.component.truck import Truck

from ensemble.logic.platoon_states import (
    StandAlone,
    Platooning,
    Joining,
    Splitting,
)

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


def to_xml(data):
    return str.encode(
        '<INST nbVeh="1" val="2.00"><CREATIONS><CREATION entree="Ext_In" id="{vehid}" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="{abscissa}" acc="{acceleration}" dst="{distance}" id="{vehid}" ord="{ordinate}" tron="{link}" type="{vehtype}" vit="{speed}" voie="{lane}" z="{elevation}"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'.format(
            **data
        )
    )


@pytest.fixture
def trk01_data_test01():
    return to_xml(
        {
            "abscissa": 0,
            "acceleration": 0,
            "distance": 200,
            "driven": False,
            "elevation": 0,
            "lane": 1,
            "link": "LinkA",
            "ordinate": 100,
            "speed": 4.0,
            "vehid": 1,
            "vehtype": "PLT",
            "status": StandAlone(),
            "platoon": False,
        }
    )


@pytest.fixture
def trk02_data_test01():
    return to_xml(
        {
            "abscissa": 0,
            "acceleration": 0,
            "distance": 50,
            "driven": False,
            "elevation": 0,
            "lane": 1,
            "link": "LinkA",
            "ordinate": 100,
            "speed": 4.0,
            "vehid": 2,
            "vehtype": "PLT",
            "status": StandAlone(),
            "platoon": False,
        }
    )


def test_1(trk01_data_test01, trk02_data_test02):
    pass
    # veh = PlatoonVehicle(**truck_leader_data)
    # fgc = FrontGapState(veh)
    # fgc.update_state(veh)
    # assert veh.front_target_state == "standalone"


# @pytest.fixture
# def truck_leader_data():
#     return {
#         leader_PCM_capable=1,
#         leader_split_request=False,
#         ego_distance_gap_to_leader=0,
#         leader_id=1,
#         leader_length=5.0,
#         ego_split_request=False,
#         ego_standalone_time_gap=1,
#         front_target_state="join",
#         ego_speed=4.0,
#         ego_position=0,
#         leader_position=0,
#         desired_gap=1,
#         standalone_gap=1,
#         platoon_id=1,
#         platoon_length=1,
#         front_id=2,
#         intruder=True,
#         ego_platoon_position=1,
#         leader_platoon_position=2,
#         maximum_platoon_length=7,
#         platoon_desired_speed=50,
#         platoon_desired_time_gap=2,
#         max_connection_distance=100,
#     }

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
