**| [Overview](#overview) | [Download](#download) | [License](#license) | [Contact](#contact) |**

# ENSEMBLE Launch 

![](https://img.shields.io/badge/platform-VISSIM-blue) ![](https://img.shields.io/badge/platform-SymuVia-green) 

<img src="docs/img/logo.png" alt="drawing" align="middle" width="200" />

## Overview 

ENSEMBLE is an effort to pave the way to multibrand truck platooning. The objective of this repository is to provide a simple way to *launch* and *execute* simulations in different platforms. 

A model develeopment platform for the Drivermodel which is used within the Eurpean project of Ensemble


Here we describe how we think the structure of the joint algorithm should be. The two simulators are called and started separately and they both perform different tasks.  Each should be capable of sending and retrieving network and status data. Some Tasks are simulator dependent(e.g. retrieving data) while others are simulator independent(l e.g oop through all vehicles)


## Download

In order to install run in your command line tool:

```{bash}
git clone https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel.git
```
Or obtain direct download [here](https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/-/archive/master/ensemble_drivermodel-master.zip). 


## Install 

** Developer environment**

Be sure to obtain `python` and `pip`.  This repository as a standard python package with support for CLI interfacing to improve the interaction. 
You can try and test functionalities by installing the package in testing mode.

```
cd ensemble_driver_model 
pip install -r requirements_dev.txt 
pip install --editable . 
```
**Note:** Be sure to be in the folder before launching the `pip` instruction

## Usage 

In order to use this tool 

```
ensemble launch scenario -f path/to/simulation_file_1 path/to_simulation_file_2 -p path/to_platform/
```

## License 

The code here contained is licensed under **TBD**

## Contact 

If you run into problems or bugs, please let us know by [creating an issue](https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/issues/new) an issue in this repository.

## Credits 

This package was created with [`Cookiecutter`](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.