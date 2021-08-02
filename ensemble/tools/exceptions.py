"""
    A module containing basic exception handlers for better error detection
"""

import warnings, click


class EnsembleAPIError(Exception):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message)
        self._target_dir = target_dir

    @property
    def target_dir(self) -> str:
        return self._target_dir

    @property
    def get_messsage(self) -> str:
        (mess,) = self.args
        return mess


class EnsembleAPILoadLibraryError(EnsembleAPIError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_messsage},{self._target_dir})"


class EnsembleAPILoadFileError(EnsembleAPIError):
    def __init__(self, error_message: str, target_dir: str = "") -> None:
        super().__init__(error_message, target_dir)

    def __str__(self) -> str:
        return f"{self.get_messsage}, at: {self._target_dir}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_messsage},{self._target_dir})"


class EnsembleAPIWarning(Exception):
    """General Warnining"""

    def __init__(self, warning_message: str) -> None:
        click.echo(click.style(warning_message, fg="red", bold=True))
        warnings.warn(warning_message)
