#!/usr/bin/env python

"""Tests for `ensemble` package."""

import unittest
from click.testing import CliRunner

from ensemble import ensemble
from ensemble import cli


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli_main(self):
    def test_cli_01_main(self):
        """ Run basic call ensemble"""
        result = self.runner.invoke(cli.main)
        self.assertEqual(result.exit_code, 0)

    def test_cli_help(self):
    def test_cli_02_help(self):
        """ Run help call ensemble """
        result = self.runner.invoke(cli.main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("--help", result.output)
        self.assertIn("Show this message and exit", result.output)

    def test_cli_03_check(self):
        """ Run check command ensemble """
        result = self.runner.invoke(cli.main, ["check --help"])
