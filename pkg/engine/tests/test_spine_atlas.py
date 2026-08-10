from crunge.engine.loader.spine.spine_atlas import AtlasFile, parse_atlas

TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy.atlas"

def test_spine_atlas():
    atlas_file = parse_atlas(TEST_FILE)
    print(atlas_file)
