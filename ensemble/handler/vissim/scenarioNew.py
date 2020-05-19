"""
**Scenario Module**

    This module contains descriptions that stablish a traffic scenario. A traffic scenario for SymuVia  is regularly described by a simulation object that points towards properties of the simulation file in this case an XML.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================
from pathlib import Path
from datetime import datetime
import os

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================
from ensemble.input.scenario import Scenario

from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)

from ensemble.tools import constants as ct


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class VissimScenario(Scenario):
    """
           Scenario class for Vissim
       """

    def __init__(self, *args):
        self.bread_additional = False
        super().__init__(*args)

    @classmethod
    def create_input(cls, *args):
        """ Looks for indicated vissim scenario paths and performs validation create the scenario"""

        existing_files = [file for file in args if Path(file).exists()]

        # Filter
        find_inpx = lambda files: [x for x in files if Path(x).suffix == ".inpx"]
        find_layx = lambda files: [x for x in files if Path(x).suffix == ".layx"]
        find_csv = lambda files: [x for x in files if Path(x).suffix == ".csv"]

        if existing_files:
            # Takes first element by default
            try:
                inpx_path = find_inpx(existing_files)[0]
            except IndexError:
                raise EnsembleAPILoadFileError(f"\tProvided files do not match expected input. Provide an INPX file")
            try:
                layx_path = find_layx(existing_files)[0]
            except IndexError:
                raise EnsembleAPILoadFileError(f"\tProvided files do not match expected input. Provide an LAYX file")
            try:
                platooncsv_path = find_csv(existing_files)[0]
            except IndexError:
                EnsembleAPIWarning(f"\tNo Platoon information provided.")
                platooncsv_path = None

            return cls(inpx_path, layx_path, platooncsv_path)
        raise EnsembleAPILoadFileError(f"Provided files are not found", args)

    @property
    def filename(self):
        """ Vissim property shortcut"""
        return self.scn_file

    @property
    def filename_layx(self):
        """ Vissim property shortcut"""
        return self.layout_file

    @property
    def filename_encoded(self):
        """ Symuvia property shortcut for loading"""
        return self.scn_file.encode("UTF8")

    def filename(self, encoding: str = None):
        """
            This method returns the value of encoding of the simulation scenario under consideration

            :param encoding: enconder UTF8, defaults to None
            :type encoding: string, optional
            :return: Full path of scenario
            :rtype: string
        """
        if encoding == "UTF8":
            return self.scn_file.encode(encoding)
        return self.scn_file
