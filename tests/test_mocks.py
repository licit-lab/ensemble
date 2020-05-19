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
        self.get_bottleneck_001()
        self.get_bottleneck_002()

    def get_bottleneck_001(self):
        self.file_name = "bottleneck_001.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)
    def get_bottleneck_002(self):
        self.file_name = "TestNetwork.inpx"
        self.file_layx="TestNetwork.layx"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        file_layx_path = ("tests", "mocks", "bottlenecks", self.file_layx)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)
        self.mocks_path_layx = os.path.join(os.getcwd(), *file_layx_path )

    def test_cli_01_bottleneck_single_vehicle(self):
        """ Run: ensemble"""
        result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path])
        self.assertEqual(result.exit_code, 0)

    def test_cli_02_bottleneck_single_vehicle(self):
            """ Run: ensemble"""
            result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path,"-s",self.mocks_path_layx])
            self.assertEqual(result.exit_code, 0)
runner = CliRunner()
file_name = "TestNetwork.inpx"
file_layx="TestNetwork.layx"
file_path = ("tests", "mocks", "bottlenecks", file_name)
file_layx_path = ("tests", "mocks", "bottlenecks", file_layx)
mocks_path = os.path.join(os.getcwd(), *file_path)
mocks_path_layx = os.path.join(os.getcwd(), *file_layx_path )
runner.invoke(cli.main,["launch", "-s", mocks_path,"-s",mocks_path_layx])
