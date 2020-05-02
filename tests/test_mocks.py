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

    def get_bottleneck_001(self):
        self.file_name = "bottleneck_001.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)

    def test_cli_01_bottleneck_single_vehicle(self):
        """ Run: ensemble"""
        result = self.runner.invoke(cli.main, ["launch", "-s", self.mocks_path])
        self.assertEqual(result.exit_code, 0)
