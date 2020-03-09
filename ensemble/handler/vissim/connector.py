"""
    This module contains objects for modeling a simplified connector to handle vissim
"""


import click
from pathlib import Path
from ensemble.input.scenario import Scenario
from ensemble.tools.exceptions import EnsembleAPIWarning, EnsembleAPILoadFileError

try:
    import win32com.client as com
        from pywintypes import com_error
except ModuleNotFoundError:
    click.echo(click.style("\t Platform non compatible with Windows", fg="yellow"))

from ensemble.tools.exceptions import EnsembleAPILoadLibraryError


class ScenarioVissim(Scenario):

    @classmethod
    def create_vissim_input(cls, *args):
        """ Looks for indicated vissim scenario paths and performs validation create the scenario"""

        existing_files = [file for file in args if Path(file).exists()]

        # Filter
        find_inpx = lambda files: [x for x in files if Path(x).suffix == '.inpx']
        find_layx = lambda files: [x for x in files if Path(x).suffix == '.layx']
        find_csv = lambda files: [x for x in files if Path(x).suffix == '.csv']

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



 
class VissimConnector(object):
    """ 
        This models a connector and interactions from the API with the Vissim library. 

        :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

    def __init__(self, path: str) -> None:
        self._path = path  # "Vissim.Vissim-64.10"# path
        self.load_vissim()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryname})"

    def load_vissim(self) -> None:
        """ load Vissim COM interface"""
        try:
            lib_vissim = com.gencache.EnsureDispatch(self._path)
            click.echo(
                click.style(
                    f"\t Library successfully loaded!", fg="green", bold=True
                )
            )
        except OSError:
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        except com_error:
            click.echo(
                click.style(
                    f"\t Visssim is currently unavailable!", fg="red", bold=True
                )
            )
            lib_vissim = None
            # raise EnsembleAPILoadLibraryError("Library not found", self._path)
            pass
        self._library = lib_vissim
