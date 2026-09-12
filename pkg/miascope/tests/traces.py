"""Record traces of the sample programs for miascope tests."""
from importlib.resources import files

import crunge.mia.runtime as rt
from crunge.mia.load import expert_classes, load_source
from crunge.miascope import Trace

ASSETS = files("crunge.mia.assets")


def sample(name: str) -> str:
    return ASSETS.joinpath(name).read_text(encoding="utf-8")


def record(name: str, experts=None):
    """Run a sample program with tracing; return the solver and the loaded Trace.

    Every expert in the file is active by default, as `mia run` does it.
    """
    module = load_source(sample(name), name.replace(".", "_"), name)
    chosen = expert_classes(module) if experts is None else [getattr(module, e) for e in experts]
    sink = rt.ListSink()
    solver = rt.ProblemSolver(chosen, tracer=rt.Tracer(sink))
    assert solver.run() is rt.Status.SUCCEEDED
    return solver, Trace(sink.events)
