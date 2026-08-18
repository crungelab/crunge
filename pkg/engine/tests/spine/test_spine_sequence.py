from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

from . import resolve_spine_path

#TEST_FILE = "/home/kurt/Dev/crunge/depot/spine-runtimes/examples/dragon/export/dragon-ess.json"


def test_spine_sequence():
    path = resolve_spine_path("dragon", ext="json")
    raw = SpineSkeletonFile.load(path)
    anim = raw.animations["flying"]          # real animation name
    tl = anim.slots.get("left-wing")
    print("slot timelines object:", tl)
    print("sequence type:", type(tl.sequence) if tl else None)
    print("sequence value:", tl.sequence if tl else None)
