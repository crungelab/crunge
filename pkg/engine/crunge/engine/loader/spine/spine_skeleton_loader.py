from pathlib import Path

from crunge.engine.loader.spine.spine_converter import load_skeleton_data
from crunge.engine.loader.spine.spine_atlas_loader import SpineAtlasLoader
from crunge.engine.d2.skeleton.skeleton import Skeleton


class SpineSkeletonLoader:
    def load(self, path: Path, atlas_path: Path):
        path = Path(path)
        atlas_path = Path(atlas_path)
        if not atlas_path.is_absolute():
            atlas_path = path.parent / atlas_path

        skel_data = load_skeleton_data(path)
        #atlas = SpineAtlasLoader().load(atlas_path, skel_data)
        atlas = SpineAtlasLoader().load(atlas_path)
        atlas.resolve(skel_data)
        skeleton = Skeleton(skel_data)
        return skeleton