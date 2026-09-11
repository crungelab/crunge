"""Sample programs shipped as package data in crunge.mia.assets."""
from importlib.resources import as_file, files

ASSETS = files("crunge.mia.assets")


def sample(name: str) -> str:
    """The source text of a sample program."""
    return ASSETS.joinpath(name).read_text(encoding="utf-8")


def sample_path(name: str):
    """Context manager giving a real filesystem path to a sample, for code that needs a file."""
    return as_file(ASSETS.joinpath(name))
