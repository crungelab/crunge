"""Compile Mia source and load it as a Python module."""

from __future__ import annotations

import types
from pathlib import Path

from crunge.mia.compile.codegen.generator import generate
from crunge.mia.compile.parse.parser import parse
from crunge.mia.runtime import Agent


def load_source(source: str, name: str = "mia_program", filename: str = "<mia>") -> types.ModuleType:
    code = generate(parse(source), filename, source)
    module = types.ModuleType(name)
    module.__file__ = filename
    exec(compile(code, f"{filename}.py", "exec"), module.__dict__)
    return module


def load_file(path: str | Path) -> types.ModuleType:
    path = Path(path)
    return load_source(path.read_text(encoding="utf-8"), f"{path.stem}_mia", path.name)


def agent_classes(module: types.ModuleType) -> list[type[Agent]]:
    """Top-level agents defined by a loaded program, in source order."""
    return [
        value for value in vars(module).values()
        if isinstance(value, type) and issubclass(value, Agent) and value.__module__ == module.__name__
    ]
