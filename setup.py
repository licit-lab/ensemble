from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

with open("README.md", "r", encoding="UTF8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

with open("HISTORY.md", "r", encoding="UTF8") as history_file:
    HISTORY = history_file.read()

requirements = [
    "click>=7.0",
    "xmltodict>=0.12",
    "lxml>=4.5.0",
    "pandas>=1.0.0",
    "symupy>=0.5.0",
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
    name="ensemble",
    version="0.1.0",
    description="A command line interface to launch scenarios for the ENSEMBLE project ",
    long_description=LONG_DESCRIPTION + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    author="Andres Ladino",
    author_email="andres.ladino@univ-eiffel.fr",
    maintainer="Andres Ladino",
    maintainer_email="andres.ladino@univ-eiffel.fr",
    url="https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel",
    download_url="https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel",
    packages=find_packages(include=["ensemble", "ensemble.*"]),
    classifiers=CLASSIFIERS,
    keywords="ensemble, truck platooning",
    include_package_data=True,
    install_requires=requirements,
    entry_points={"console_scripts": ["ensemble=ensemble.cli:main"]},
    extra_require={"dev": dev_requirements},
    python_requires=">=3.7",
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    zip_safe=False,
)
