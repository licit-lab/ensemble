#!/usr/bin/env python

"""Tests for `ensemble` package."""

import os
import unittest
from click.testing import CliRunner

from ensemble import ensemble
from ensemble import cli


class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.get_bottleneck_symuvia_001()
        self.get_bottleneck_symuvia_002()
        self.get_bottleneck_vissim_01()

    def get_bottleneck_symuvia_001(self):
        self.file_name_btl01 = "bottleneck_001.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name_btl01)
        self.mocks_path_btl01 = os.path.join(os.getcwd(), *file_path)

    def get_bottleneck_symuvia_002(self):
        self.file_name_btl02 = "bottleneck_001.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name_btl02)
        self.mocks_path_btl02 = os.path.join(os.getcwd(), *file_path)

    def get_bottleneck_vissim_01(self):
        self.file_name = "TestNetwork.inpx"
        self.file_layx = "TestNetwork.layx"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        file_layx_path = ("tests", "mocks", "bottlenecks", self.file_layx)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)
        self.mocks_path_layx = os.path.join(os.getcwd(), *file_layx_path)

    def test_cli_symuvia_01_bottleneck_single_vehicle(self):
        """ Run: ensemble"""
        result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path_btl01])
        self.assertEqual(result.exit_code, 0)

    def test_cli_symuvia_02_bottleneck_multiple_vehicles(self):
        """ Run: ensemble"""
        result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path_btl02])
        self.assertEqual(result.exit_code, 0)

    def test_cli_02_bottleneck_single_vehicle(self):

        """ Run: ensemble"""
        result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path, "-s", self.mocks_path_layx])
        self.assertEqual(result.exit_code, 0)


