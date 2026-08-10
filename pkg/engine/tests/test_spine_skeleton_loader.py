from crunge.engine.loader.spine.spine_skeleton_loader import SpineSkeletonLoader

TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-pro.json"


def test_spine_skeleton_loader():
    loader = SpineSkeletonLoader()
    skeleton = loader.load(TEST_FILE, "spineboy.atlas")
    print(skeleton)
