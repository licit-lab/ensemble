"""
**Scenario Module**

    This module contains descriptions that stablish a traffic scenario. A traffic scenario for SymuVia  is regularly described by a simulation object that points towards properties of the simulation file in this case an XML. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================
from pathlib import Path

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================
from ensemble.input.scenario import Scenario


from ensemble.tools.exceptions import (
    EnsembleAPIWarning,
    EnsembleAPILoadFileError,
    EnsembleAPILoadLibraryError,
)


# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymuviaScenario(Scenario):
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
