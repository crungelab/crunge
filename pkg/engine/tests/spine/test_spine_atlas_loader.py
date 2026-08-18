from crunge.engine.loader.spine.spine_atlas_loader import SpineAtlasLoader

from . import resolve_spine_path


def test_spine_atlas_loader():
    loader = SpineAtlasLoader()
    path = resolve_spine_path("spineboy", version="", ext="atlas")
    atlas = loader.load(path)
    print(atlas)
