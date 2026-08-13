from crunge.engine.loader.spine.spine_skeleton_loader import SpineSkeletonLoader
from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

TEST_FILE = "/home/kurt/Dev/crunge/depot/spine-runtimes/examples/dragon/export/dragon-ess.json"


def test_spine_sequence():
    raw = SpineSkeletonFile.load(TEST_FILE)
    anim = raw.animations["flying"]          # real animation name
    tl = anim.slots.get("left-wing")
    print("slot timelines object:", tl)
    print("sequence type:", type(tl.sequence) if tl else None)
    print("sequence value:", tl.sequence if tl else None)
