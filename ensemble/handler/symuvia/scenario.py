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
from lxml import etree

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

            scenario = cls(xml_path, None, platooncsv_path)
            scenario.load_xml_tree()
            return scenario
        raise EnsembleAPILoadFileError(f"Provided files are not found", args)

    def load_xml_tree(self) -> None:
        """ Load XML file_name
        """
        # TODO: Add validation with DTD
        tree = etree.parse(self.filename())
        root = tree.getroot()
        self.xmltree = root

    def get_simulation_parameters(self) -> tuple:
        """ Get simulation parameters

        :return: tuple with XML dictionary containing parameters
        :rtype: tuple
        """
        branch_tree = "SIMULATIONS"
        sim_params = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(par.attrib for par in sim_params)

    def get_vehicletype_information(self) -> tuple:
        """ Get the vehicle parameters

        :return: tuple of dictionaries containing vehicle parameters
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/TYPES_DE_VEHICULE"
        vehicle_types = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(v.attrib for v in vehicle_types)

    def get_network_endpoints(self) -> tuple:
        """ Get networks endpoint names

        :return: tuple containing endpoint names
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/EXTREMITES"
        end_points = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(ep.attrib["id"] for ep in end_points)

    def get_network_links(self) -> tuple:
        """ Get network link names

        :return: tuple containing link names
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/TRONCONS"
        links = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(ep.attrib["id"] for ep in links)

    def get_simulation_steps(self, simid: int = 0) -> range:
        """Get simulation steps for an simulation. specify the simulation id  via an integer value

        :param simid: simulation id , defaults to 0
        :type simid: int, optional
        :return:
        :rtype: range
        """
        t1 = datetime.strptime(self.get_simulation_parameters()[simid].get("debut"), ct.HOUR_FORMAT)
        t2 = datetime.strptime(self.get_simulation_parameters()[simid].get("fin"), ct.HOUR_FORMAT)
        t = t2 - t1
        n = t.seconds / float(self.get_simulation_parameters()[simid].get("pasdetemps"))
        return range(int(n))

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
