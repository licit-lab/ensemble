import warnings, click


class EnsembleAPIWarning(Exception):
    """ General Warnining
    """

    def __init__(self, warning_message: str) -> None:
        click.echo(click.style(warning_message, fg="red"))
        warnings.warn(warning_message)
