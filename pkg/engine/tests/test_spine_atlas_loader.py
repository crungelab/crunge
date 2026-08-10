from crunge.engine.loader.spine.spine_atlas_loader import SpineAtlasLoader

TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy.atlas"


def test_spine_atlas_loader():
    loader = SpineAtlasLoader()
    atlas = loader.load(TEST_FILE)
    print(atlas)
