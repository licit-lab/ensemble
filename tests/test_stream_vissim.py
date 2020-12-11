import pytest

from ensemble.handler.vissim.stream import SimulatorRequest


@pytest.fixture
def vissim_dict():
    return {
        "CoordFrontX": 421.31564190349957,
        "Acceleration": -0.0,
        "Pos": 16.25355208592856,
        "No": 1,
        "CoordFrontY": -979.2497097242955,
        "Lane\\Link\\No": 6,
        "VehType": "630",
        "Speed": 83.93049031871615,
        "Lane\\Index": 1,
    }


@pytest.fixture
def output_reference():
    return {
        "abscissa": 421.31564190349957,
        "acceleration": -0.0,
        "distance": 16.25355208592856,
        "driven": False,
        "elevation": 0.0,
        "lane": 1,
        "link": "6",
        "ordinate": -979.2497097242955,
        "speed": 23.314025088532265,
        "vehid": 1,
        "vehtype": "630",
    }


@pytest.fixture
def two_vehicle_dictionaries():
    vehsAttributesNamesVissim = (
        "CoordFrontX",
        "Acceleration",
        "Pos",
        "No",
        "CoordFrontY",
        "Lane\\Link\\No",
        "VehType",
        "Speed",
        "Lane\\Index",
    )
    vissim_data = (
        (
            410.29939091394306,
            -0.0,
            39.56757717446082,
            1,
            -958.7025449572575,
            6,
            "630",
            83.93049031871615,
            1,
        ),
        (
            425.80857613274515,
            -0.25,
            6.745019515178477,
            2,
            -987.6297892979444,
            6,
            "630",
            83.03282745299681,
            1,
        ),
    )
    vehData = [
        dict(zip(vehsAttributesNamesVissim, item)) for item in vissim_data
    ]
    return vehData


@pytest.fixture
def two_vehicle_formatted_dictionaries():
    return [
        {
            "abscissa": 410.29939091394306,
            "acceleration": -0.0,
            "distance": 39.56757717446082,
            "driven": False,
            "elevation": 0,
            "lane": 1,
            "link": "6",
            "ordinate": -958.7025449572575,
            "speed": 23.314025088532265,
            "vehid": 1,
            "vehtype": "630",
        },
        {
            "abscissa": 425.80857613274515,
            "acceleration": -0.25,
            "distance": 6.745019515178477,
            "driven": False,
            "elevation": 0,
            "lane": 1,
            "link": "6",
            "ordinate": -987.6297892979444,
            "speed": 23.064674292499113,
            "vehid": 2,
            "vehtype": "630",
        },
    ]


@pytest.fixture
def simrequest():
    return SimulatorRequest()


def test_parser_convert(vissim_dict, output_reference):
    outdict = SimulatorRequest.transform(vissim_dict)
    assert set(outdict.items()) == set(output_reference.items())


def test_parser_conver(
    simrequest, two_vehicle_dictionaries, two_vehicle_formatted_dictionaries
):
    simrequest.query = two_vehicle_dictionaries
    veh_data = simrequest.get_vehicle_data()
    assert (
        all(
            [
                set(a.items()) == set(b.items())
                for a, b in zip(veh_data, two_vehicle_formatted_dictionaries)
            ]
        )
        == True
    )
