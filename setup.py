#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md", "r") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "pandas>=1.0"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Andres Ladino",
    author_email="andres.ladino@ifsttar.fr",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A command line interface to launch scenarios for the ENSEMBLE project ",
    entry_points={"console_scripts": ["ensemble=ensemble.cli:main"]},
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="ensemble",
    name="ensemble",
    packages=find_packages(include=["ensemble", "ensemble.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/andres.ladino-ifsttar/ensemble",
    version="0.1.0",
    zip_safe=False,
)
