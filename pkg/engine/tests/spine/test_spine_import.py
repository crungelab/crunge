from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

from . import resolve_spine_path


def test_spine_import():
    path = resolve_spine_path("spineboy", ext="json")
    spine_file = SpineSkeletonFile.load(path)
    print(spine_file)
