#!/usr/bin/env python

"""Tests for `ensemble` package."""

import os
import pytest
from click.testing import CliRunner

from ensemble import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def bottleneck_001():
    file_path = ("tests", "mocks", "bottlenecks", "bottleneck_001.xml")
    return os.path.join(os.getcwd(), *file_path)


@pytest.fixture
def bottleneck_002():
    file_path = ("tests", "mocks", "bottlenecks", "bottleneck_002.xml")
    return os.path.join(os.getcwd(), *file_path)


@pytest.fixture
def botleneck_vissim_01():
    file_path = ("tests", "mocks", "bottlenecks", "TestNetwork.inpx")
    file_layx_path = ("tests", "mocks", "bottlenecks", "TestNetwork.layx")
    mocks_path = os.path.join(os.getcwd(), *file_path)
    mocks_path_layx = os.path.join(os.getcwd(), *file_layx_path)
    return mocks_path, mocks_path_layx


def test_cli_symuvia_01_bottleneck_single_vehicle(runner, bottleneck_001):
    """ Run: ensemble launch -s path/to/bottleneck01"""
    result = runner.invoke(cli.main, ["launch", "-s", bottleneck_001])
    result.exit_code == 0


def test_cli_symuvia_02_bottleneck_multiple_vehicles(runner, bottleneck_002):
    """ Run: ensemble launch -s path/to/bottleneck02"""
    result = runner.invoke(cli.main, ["launch", "-s", bottleneck_002])
    result.exit_code == 0


def test_cli_vissim_bottleneck_single_vehicle(runner, botleneck_vissim_01):
    """ Run: ensemble -s path/to/inpx -s path/to/layx"""
    result = runner.invoke(
        cli.main,
        ["launch", "-s", botleneck_vissim_01[0], "-s", botleneck_vissim_01[1]],
    )
    result.exit_code == 0
