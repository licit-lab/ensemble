import pytest
from mypackage.frontgap2 import FrontGapState
from mypackage.frontgap2 import RearGapState
from mypackage.vehicle2 import PlatoonVehicle
def test_1_standalone_no_follower():
    veh = PlatoonVehicle(rear_target_state = "standalone",
    ego_split_request = False,
    follower_id	=	-1	,
    follower_PCM_capable	=	False	,
    follower_front_target_state	=	-1	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"
def test_2_standalone_no_equipped_follower():
    veh = PlatoonVehicle(rear_target_state	=	"standalone",
    ego_split_request	=	False,
    follower_id	=	200,
    follower_PCM_capable	=	False,
    follower_front_target_state	=	-1,
    follower_split_request	=	False)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"
def test_3_standalone_not_yet_join():
    veh = PlatoonVehicle(
    rear_target_state	=	"standalone"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"standalone"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"
def test_4_standalone_to_join():
    veh = PlatoonVehicle(
    rear_target_state	=	"standalone"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"join"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "join"
def test_5_join_to_standalone():
    veh = PlatoonVehicle(
    rear_target_state	=	"join"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"standalone"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"


def test_6_join_to_platoon():
    veh = PlatoonVehicle(
    rear_target_state	=	"join"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"platoon"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "platoon"
def test_7_platoon_to_backsplit_ego_wants_to_leave():
    veh = PlatoonVehicle(
    rear_target_state	=	"platoon"	,
    ego_split_request	=	True	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"platoon"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "backsplit"
def test_8_platoon_to_backsplit_follower_wants_to_leave():
    veh = PlatoonVehicle(
    rear_target_state	=	"platoon"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"frontsplit"	,
    follower_split_request	=	True	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "backsplit"
def test_9_backsplit_to_standalone():
    veh = PlatoonVehicle(
    rear_target_state	=	"backsplit"	,
    ego_split_request	=	True	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"standalone"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"
def test_10_backsplit_to_standalone():
    veh = PlatoonVehicle(
    rear_target_state	=	"backsplit"	,
    ego_split_request	=	False	,
    follower_id	=	200	,
    follower_PCM_capable	=	True	,
    follower_front_target_state	=	"standalone"	,
    follower_split_request	=	True	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "standalone"
def test_11_stay_in_platoon_during_cutin():
    veh = PlatoonVehicle(
    rear_target_state	=	"platoon"	,
    ego_split_request	=	False	,
    follower_id	=	999	,
    follower_PCM_capable	=	False	,
    follower_front_target_state	=	"cutin"	,
    follower_split_request	=	False	)
    rgc = RearGapState(veh)
    rgc.update_state(veh)
    assert veh.rear_target_state == "platoon"




