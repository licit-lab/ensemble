#!/usr/bin/env python

"""Tests for `ensemble` package."""

import unittest
from click.testing import CliRunner

from ensemble import ensemble
from ensemble import cli


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli_01_main(self):
        """ Run: ensemble"""
        result = self.runner.invoke(cli.main)
        self.assertEqual(result.exit_code, 0)

    def test_cli_02_main_help(self):
        """ Run: ensemble --help """
        result = self.runner.invoke(cli.main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--help", result.output)
        self.assertIn("Show this message and exit", result.output)

    def test_cli_03_check(self):
        """Run: ensemble check"""
        result = self.runner.invoke(cli.main, ["check"])
        self.assertIn("Error: Scenario file(s) is an empty list", result.output)

    def test_cli_04_check_help(self):
        """Run: ensemble check --help"""
        result = self.runner.invoke(cli.main, ["check", "--help"])
        self.assertIn("Show this message and exit", result.output)
