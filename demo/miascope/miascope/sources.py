"""Where miascope's traces come from: files on disk, or samples in crunge.mia.assets.

A bare name like `blox.mia` or `blox.miatrace` refers to a sample asset; anything
else is a path. A `.mia` program is compiled and run with tracing on the spot,
so its trace always matches the current runtime. A `.miatrace` file is loaded
as recorded.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from dataclasses import dataclass

from .model import Trace

ASSETS = files("crunge.mia.assets")
SUFFIXES = (".mia", ".miatrace")
DEFAULT_SAMPLE = "blox.mia"


@dataclass
class Source:
    """A trace, plus the live plan when miascope ran the program itself.

    A trace read from disk has the text of each action but not the functions
    behind them, so its plan can be shown and not replayed.
    """

    name: str
    trace: Trace
    plan: object | None = None   # a crunge.mia.runtime.Plan when it can be replayed

    @property
    def runnable(self) -> bool:
        return self.plan is not None and len(self.plan) > 0


def sample_names() -> list[str]:
    return sorted(item.name for item in ASSETS.iterdir() if item.name.endswith(SUFFIXES))


def load_source_text(source: str) -> tuple[str, str]:
    asset = ASSETS.joinpath(source)
    if "/" not in source and "\\" not in source and asset.is_file():
        return asset.read_text(encoding="utf-8"), source
    path = Path(source)
    return path.read_text(encoding="utf-8"), path.name


def load(source: str) -> Source:
    text, name = load_source_text(source)
    if name.endswith(".mia"):
        return record_program(text, name)
    return Source(name, Trace.loads(text))


def load_trace(source: str) -> Trace:
    return load(source).trace


def record_program(source: str, name: str = "<mia>") -> Source:
    """Compile and run a Mia program with tracing, and keep its plan."""
    # Imported here so the viewer's model never depends on the runtime.
    import crunge.mia.runtime as rt
    from crunge.mia.load import expert_classes, load_source

    module = load_source(source, Path(name).stem + "_mia", name)
    experts = expert_classes(module)
    if not experts:
        raise ValueError(f"{name} defines no experts")
    sink = rt.ListSink()
    # Every expert in the file is active, as `mia run` does it.
    solver = rt.ProblemSolver(experts, tracer=rt.Tracer(sink))
    solver.run()
    return Source(name, Trace(sink.events), solver.plan)
