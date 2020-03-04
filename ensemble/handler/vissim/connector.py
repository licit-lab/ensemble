"""
    This module contains objects for modeling a simplified connector to handle vissim
"""


from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click

from ensemble.tools.exceptions import EnsembleAPILoadLibraryError


class VissimConnector(object):
    def __init__(self, path: str) -> None:
        self._path = path
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
        self._library = lib_vissim
