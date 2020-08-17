**| [Overview](#overview) | [Download](#download) | [Install](#install) | [Use](#use) | [License](#license) | [Contact](#contact) |**

# ENSEMBLE Launch 

![](https://img.shields.io/badge/platform-VISSIM-blue) ![](https://img.shields.io/badge/platform-SymuVia-green) ![](https://img.shields.io/badge/Documentation-here-green)

A CLI implementing Multibrand platooning for ENSEMBLE within traffic simulators. Please find more information in the [documentation](http://paco.hamers-tno.pages.ci.tno.nl/ensemble_drivermodel/)

<img src="docs/source/img/logo.png" alt="drawing" align="middle" width="200" />

## Overview 

[ENSEMBLE](https://platooningensemble.eu) is an effort to pave the way to multibrand truck platooning. The objective of this repository is to provide a simple way to *launch* and *execute* simulations in different traffic simulation platforms. 

This software application describes a model for the platooning driver model which is used within the Eurpean project of [ENSEMBLE](https://platooningensemble.eu).

Here we describe how we think the structure of the cooperation between the specification adn the traffic simulation platform is implemented.


## Download

In order to install run in your command line tool:

```{bash}
git clone https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel.git
```
Or obtain direct download [here](https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/-/archive/master/ensemble_drivermodel-master.zip). 


## Install 

**Developer environment**

Be sure to obtain `python` and `pip`.  This repository as a standard python package with support for CLI interfacing to improve the interaction. 
You can try and test functionalities by installing the package in testing mode.

```
cd ensemble_driver_model 
pip install -r requirements_dev.txt 
pip install --editable . 
```
**Note:** Be sure to be in the folder before launching the `pip` instruction

## Use 

In order to use this tool, first check the help options via:

```
ensemble --help
```

Which should print the available options 

```
❯ ensemble --help
Usage: ensemble [OPTIONS] COMMAND [ARGS]...

  Scenario launcher for ENSEMBLE simulations

Options:
  --verbose
  --platform TEXT  'symuvia' or 'vissim'
  --help           Show this message and exit.

Commands:
  check   Diagnoses files consistancy and simulator availability
  launch  Launches an escenario for a specific platform
```

Check possible options by typing `ensemble launch` or `ensemble check`. Execute an scenario via 

```
ensemble launch -s 'file_scenario.inpx' -s 'file_layout.layx' -l 'C:\my\path\to\vissim'
```

## Documentation 

Documentation is available [here](http://paco.hamers-tno.pages.ci.tno.nl/ensemble_drivermodel/) or in the `docs` folder. In order to build the documentation 

```
make docs 
```

## License 

The code here contained is licensed under **TBD**

## Contact 

If you run into problems or bugs, please let us know by [creating an issue](https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/issues/new) an issue in this repository.

## Credits 

This package was created with [`Cookiecutter`](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.