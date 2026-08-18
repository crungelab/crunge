
import pytest

from crunge.engine.loader.spine.spine_skeleton_loader import SpineSkeletonLoader

from . import create_spine_path


@pytest.mark.parametrize("name,version", [
    ("spineboy", "ess"),
    #("spineboy", "pro"),
])
def test_load_skeleton(name, version):
    loader = SpineSkeletonLoader()
    path = create_spine_path(name, version)
    skeleton = loader.load(path, f"{name}.atlas")
    print(skeleton)

"""
class TestSpineLoading:
    name = "spineboy"
    version = "ess"

    def test_load_skeleton(self):
        loader = SpineSkeletonLoader()
        name = self.name
        version = self.version
        # path = f"${{spines}}/{name}/export/{name}-{version}.json"
        path = create_spine_path(name, version)
        skeleton = loader.load(path, f"{name}.atlas")
        print(skeleton)
"""

"""
def test_spine_skeleton_loader():
    loader = SpineSkeletonLoader()
    skeleton = loader.load(TEST_FILE, "spineboy.atlas")
    print(skeleton)
"""
