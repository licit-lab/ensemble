"""
    This module contains objects for modeling a simplified connector to handle symuvia 
"""


from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click

from ensemble.tools.exceptions import EnsembleAPILoadLibraryError


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
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        self._library = lib_symuvia
