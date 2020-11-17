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
def bottleneck01():
    return os.path.join(
        os.getcwd(), "tests", "mocks", "bottlenecks", "bottleneck_001.xml"
    )


def test_cli_01_main(runner):
    """ Run: ensemble"""
    result = runner.invoke(cli.main)
    result.exit_code == 0


def test_cli_02_main_help(runner):
    """ Run: ensemble --help """
    result = runner.invoke(cli.main, ["--help"])
    result.exit_code == 0
    "--help" in result.output
    "Show this message and exit" in result.output


def test_cli_03_check(runner):
    """Run: ensemble check"""
    result = runner.invoke(cli.main, ["check"])
    "Error: \tScenario file(s) is an empty list" == result.output


def test_cli_04_check(runner, bottleneck01):
    """Run: ensemble check"""
    result = runner.invoke(cli.main, ["check", "-s", bottleneck01])
    f"Input File: {bottleneck01} Found\n" in result.output


def test_cli_04_check_help(runner):
    """Run: ensemble check --help"""
    result = runner.invoke(cli.main, ["check", "--help"])
    "Show this message and exit" in result.output


def test_cli_05_launch(runner):
    """Run: ensemble launch"""
    result = runner.invoke(cli.main, ["launch"])


def test_cli_06_launch_help(runner):
    """Run: ensemble check --help"""
    result = runner.invoke(cli.main, ["launch", "--help"])
    "Show this message and exit" == result.output


def test_cli_07_check_files_not_found(runner):
    """Run: ensemble check -s fileA.csv -s fileB.xml"""
    result = runner.invoke(
        cli.main, ["check", "-s", "fileA.csv", "-s", "fileB.xml"]
    )
    "Input File: fileA.csv. Not Found " in result.output
    "Input File: fileB.xml. Not Found " in result.output


def test_cli_08_launch_files_check_files_not_found(runner):
    """Run: ensemble lauch -s fileA.csv -s fileB.xml --check"""
    result = runner.invoke(
        cli.main, ["launch", "-s", "fileA.csv", "-s", "fileB.xml", "--check"]
    )
    "Input File: fileA.csv. Not Found " == result.output
    "Input File: fileB.xml. Not Found " == result.output
