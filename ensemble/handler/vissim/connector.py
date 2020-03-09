"""
    This module contains objects for modeling a simplified connector to handle vissim
"""


import click

try:
    import win32com.client as com
    from pywintypes import com_error
except ModuleNotFoundError:
    click.echo(click.style("\t Platform non compatible with Windows", fg="yellow"))

from ensemble.tools.exceptions import EnsembleAPILoadLibraryError


class VissimConnector(object):
    """ 
        This models a connector and interactions from the API with the Vissim library. 

        :raises EnsembleAPILoadLibraryError: Raises error when library cannot be loaded
    """

    def __init__(self, path: str) -> None:
        self._path = path #"Vissim.Vissim-64.10"# path
        self.load_vissim()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryname})"

    def load_vissim(self) -> None:
        """ load Vissim COM interface"""
        try:
            lib_vissim = com.gencache.EnsureDispatch(self._path)
            click.echo(click.style(f"\t Library successfully loaded!", fg="green", bold=True))
        except OSError:
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        except com_error:
            #raise EnsembleAPILoadLibraryError("Library not found", self._path)
            pass

        self._library = lib_vissim
