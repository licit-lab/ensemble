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
    "numpy>=1.16",
    "lxml>=4.3.3",
    "networkx>=2.5",
    "matplotlib>=3.0.0",
    "pandas>=version='1.0.1'",
    "click>=8.0",
    "python-decouple>=3.3",
]

test_requirements = [
    "pytest>=3",
]

dev_requirements = [
    "sphinx==3.2.1",
    "recommonmark==0.6.0",
    "pytest==6.1.1",
    "bump2version==version='1.0.1'",
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
    version="1.0.1",
    description="A command line interface to launch scenarios for the ENSEMBLE project ",
    long_description=LONG_DESCRIPTION + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    author="Andres Ladino",
    author_email="andres.ladino@univ-eiffel.fr",
    maintainer="Andres Ladino",
    maintainer_email="andres.ladino@univ-eiffel.fr",
    url="https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel",
    download_url="https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel",
    packages=find_packages(
        include=["ensemble", "ensemble.*", "*.ini", "*.xml", "*.xsd"]
    ),
    classifiers=CLASSIFIERS,
    keywords="ensemble, truck platooning",
    include_package_data=True,
    package_data={"": ["*.ini", "*.xml", "*.xsd"],},
    install_requires=requirements,
    entry_points={"console_scripts": ["ensemble=ensemble.cli:main"]},
    extra_require={"dev": dev_requirements},
    python_requires=">=3.7",
    test_suite="tests",
    tests_require=test_requirements,
    zip_safe=False,
)
