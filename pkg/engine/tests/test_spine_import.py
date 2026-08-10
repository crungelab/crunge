from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-pro.json"


def test_spine_import():
    spine_file = SpineSkeletonFile.load(TEST_FILE)
    print(spine_file)
