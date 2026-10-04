"""Loading traces from samples and files."""
import pytest

from crunge.miascope import Trace
from crunge.miascope.sources import DEFAULT_SAMPLE, load_trace, record_program, sample_names
from tests.traces import record, sample


def test_samples_include_the_programs():
    names = sample_names()
    assert DEFAULT_SAMPLE in names
    assert {"blox.mia", "counting.mia"} <= set(names)


def test_a_sample_program_is_recorded_fresh():
    trace = load_trace("blox.mia")
    space = trace.top
    assert space.expert == "Blox" and space.solution.cost == 4

def test_trace_files_load_by_path(tmp_path):
    _, recorded = record("counting.mia")
    path = tmp_path / "counting.miatrace"
    path.write_text("".join(__import__("json").dumps(e) + "\n" for e in recorded.events), encoding="utf-8")
    trace = load_trace(str(path))
    assert len(trace.events) == len(recorded.events)
    assert Trace.loads(path.read_text()).top.expert == "Counting"


def test_a_program_file_by_path_is_recorded(tmp_path):
    path = tmp_path / "mine.mia"
    path.write_text(sample("trip.mia"), encoding="utf-8")
    assert load_trace(str(path)).top.expert == "Trip"


def test_errors_surface():
    with pytest.raises(OSError):
        load_trace("no/such/file.miatrace")
    with pytest.raises(ValueError, match="defines no experts"):
        record_program("class Block\n", "empty.mia")
