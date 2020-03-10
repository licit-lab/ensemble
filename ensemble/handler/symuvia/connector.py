"""
    This module contains objects for modeling a simplified connector to handle symuvia 
"""


from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click

from pathlib import Path

from ensemble.input.scenario import Scenario
from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)


class ScenarioSymuVia(Scenario):
    """ 
        Scenario class for Vissim
    """

    @classmethod
    def create_input(cls, *args):
        """ Looks for indicated symuvia scenario paths and performs validation create the scenario"""

        existing_files = [file for file in args if Path(file).exists()]

        # Filter
        find_xml = lambda files: [x for x in files if Path(x).suffix == ".xml"]
        find_csv = lambda files: [x for x in files if Path(x).suffix == ".csv"]

        if existing_files:
            # Takes first element by default
            try:
                xml_path = find_xml(existing_files)[0]
            except IndexError:
                raise EnsembleAPILoadFileError(f"\tProvided files do not match expected input. Provide an XML file")
            try:
                platooncsv_path = find_csv(existing_files)[0]
            except IndexError:
                EnsembleAPIWarning(f"\tNo Platoon information provided.")
                platooncsv_path = None

            return cls(xml_path, None, platooncsv_path)
        raise EnsembleAPILoadFileError(f"Provided files are not found", args)

    @property
    def filename(self):
        """ Symuvia property shortcut"""
        return self.scn_file

    @property
    def filename_encoded(self):
        """ Symuvia property shortcut for loading"""
        return self.scn_file.encode("UTF8")


class SymuviaConnector(object):
    """ 
        This models a connector and interactions from the API with the Symuvia library. 

        :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self.load_symuvia()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryname})"

    def load_symuvia(self) -> None:
        """ load SymuVia shared library """
        try:
            lib_symuvia = cdll.LoadLibrary(self._path)
            click.echo(click.style(f"\t Library successfully loaded!", fg="green", bold=True))
        except OSError:
            click.echo(click.style(f"\t SymuVia is currently unavailable!", fg="red", bold=True,))
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        self._library = lib_symuvia

    def load_scenario(self, scenario):
        """ checks existance and load scenario into 
        """
        if isinstance(scenario, ScenarioSymuVia):
            try:
                self._library.SymLoadNetworkEx(self.filename_encoded)
                return
            except:
                raise EnsembleAPILoadFileError(f"\t Simulation could not be loaded")
        EnsembleAPIWarning(f"\tSimulation could not be loaded.")
