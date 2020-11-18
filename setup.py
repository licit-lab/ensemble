#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md", "r", encoding="UTF8") as history_file:
    history = history_file.read()

requirements = [
    "click>=7.0",
    "xmltodict>=0.12",
    "lxml>=4.5.0",
    "pandas>=1.0.0",
    "symupy>=0.4.2",
    "networkx>=2.5",
    "python-decouple>=3.3",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

dev_requirements = [
    "sphinx==3.2.1",
    "recommonmark==0.6.0",
    "pytest==6.1.1",
    "bump2version==1.0.0",
    "twine==3.2.0",
    "black==19.10b0",
    "pylint==2.6.0",
    "sphinx-rtd-theme==0.5.0",
    "tox==3.20.0",
    "coverage==5.3",
    "flake8==3.8.4",
]

setup(
    author="Andres Ladino",
    author_email="andres.ladino@ifsttar.fr",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
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
    test_suite="tests",
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extra_require={"dev": dev_requirements},    
    url="https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel",
    version="0.1.0",
    zip_safe=False,
)
