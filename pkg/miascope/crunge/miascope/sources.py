"""Where miascope's traces come from: files on disk, or samples in crunge.mia.assets.

A bare name like `blox.mia` or `blox.miatrace` refers to a sample asset; anything
else is a path. A `.mia` program is compiled and run with tracing on the spot,
so its trace always matches the current runtime. A `.miatrace` file is loaded
as recorded.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from .model import Trace

ASSETS = files("crunge.mia.assets")
SUFFIXES = (".mia", ".miatrace")
DEFAULT_SAMPLE = "blox.mia"


def sample_names() -> list[str]:
    return sorted(item.name for item in ASSETS.iterdir() if item.name.endswith(SUFFIXES))


def load_trace(source: str) -> Trace:
    asset = ASSETS.joinpath(source)
    if "/" not in source and "\\" not in source and asset.is_file():
        text, name = asset.read_text(encoding="utf-8"), source
    else:
        path = Path(source)
        text, name = path.read_text(encoding="utf-8"), path.name
    if name.endswith(".mia"):
        return record_program(text, name)
    return Trace.loads(text)


def record_program(source: str, name: str = "<mia>") -> Trace:
    """Compile and run a Mia program with tracing, and return its trace."""
    # Imported here so the viewer's model never depends on the runtime.
    import crunge.mia.runtime as rt
    from crunge.mia.load import agent_classes, load_source

    module = load_source(source, Path(name).stem + "_mia", name)
    agents = agent_classes(module)
    if not agents:
        raise ValueError(f"{name} defines no agents")
    sink = rt.ListSink()
    rt.AgentHost(agents[0], tracer=rt.Tracer(sink)).run()
    return Trace(sink.events)
