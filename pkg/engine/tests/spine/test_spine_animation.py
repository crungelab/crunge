from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

from . import resolve_spine_path


def test_spine_animation():
    path = resolve_spine_path("spineboy")
    raw = SpineSkeletonFile.load(path)
    # print(raw)

    walk = raw.animations["walk"]
    print(
        "front-thigh rotate keyframes:",
        walk.bones.get("front-thigh", None) and walk.bones["front-thigh"].rotate,
    )
    print("ik constraints in walk animation:", walk.ik)
    print("ik constraints defined on skeleton:", raw.ik)
