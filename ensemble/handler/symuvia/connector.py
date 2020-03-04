"""
    This module contains objects for modeling a simplified connector to handle symuvia 
"""


from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double

from ensemble.tools.exceptions import EnsembleAPILoadLibraryError


class SymuviaConnector(object):
    def __init__(self, path: str) -> None:
        self.load_symuvia(path)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryname})"

    def load_symuvia(self) -> None:
        """ load SymuVia shared library """
        try:
            lib_symuvia = cdll.LoadLibrary(self._path)
        except OSError:
            raise EnsembleAPILoadLibraryError("Library not found", self._path)
        self._library = lib_symuvia
