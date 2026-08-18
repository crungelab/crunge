from crunge.engine.loader.spine.spine_atlas_file import AtlasFile, parse_atlas

from . import resolve_spine_path


def test_spine_atlas_file():
    path = resolve_spine_path("spineboy", version="", ext="atlas")
    atlas_file = parse_atlas(path)
    print(atlas_file)
