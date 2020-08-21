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
        self.assertIn("Error: \tScenario file(s) is an empty list", result.output)

    def test_cli_04_check_help(self):
        """Run: ensemble check --help"""
        result = self.runner.invoke(cli.main, ["check", "--help"])
        self.assertIn("Show this message and exit", result.output)

    def test_cli_05_launch(self):
        """Run: ensemble launch"""
        result = self.runner.invoke(cli.main, ["launch"])

    def test_cli_06_launch_help(self):
        """Run: ensemble check --help"""
        result = self.runner.invoke(cli.main, ["launch", "--help"])
        self.assertIn("Show this message and exit", result.output)

    def test_cli_07_check_files_not_found(self):
        """Run: ensemble check -s fileA.csv -s fileB.xml"""
        result = self.runner.invoke(cli.main, ["check", "-s", "fileA.csv", "-s", "fileB.xml"])
        self.assertIn("Input File: fileA.csv. Not Found ", result.output)
        self.assertIn("Input File: fileB.xml. Not Found ", result.output)

    def test_cli_08_launch_files_check_files_not_found(self):
        """Run: ensemble lauch -s fileA.csv -s fileB.xml --check"""
        result = self.runner.invoke(cli.main, ["launch", "-s", "fileA.csv", "-s", "fileB.xml", "--check"])
        self.assertIn("Input File: fileA.csv. Not Found ", result.output)
        self.assertIn("Input File: fileB.xml. Not Found ", result.output)