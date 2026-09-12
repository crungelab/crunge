"""Record traces of the sample programs for miascope tests."""
from importlib.resources import files

import crunge.mia.runtime as rt
from crunge.mia.load import expert_classes, load_source
from crunge.miascope import Trace

ASSETS = files("crunge.mia.assets")


def sample(name: str) -> str:
    return ASSETS.joinpath(name).read_text(encoding="utf-8")


def record(name: str):
    """Run a sample program with tracing; return the host and the loaded Trace."""
    module = load_source(sample(name), name.replace(".", "_"), name)
    sink = rt.ListSink()
    host = rt.ProblemSolver(expert_classes(module)[0], tracer=rt.Tracer(sink))
    assert host.run() is rt.Status.SUCCEEDED
    return host, Trace(sink.events)
