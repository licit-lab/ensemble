"""
**Scenario Module**

    This module contains descriptions that establish a traffic scenario.
    A traffic scenario for Vissim  is regularly described by a an network files(.inpx) and a layoutfile(.layx).
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================
import click
from pathlib import Path
from ensemble.input.scenario import Scenario
from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)




# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


"""
    This module contains objects for modeling a simplified connector to handle vissim
"""

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


