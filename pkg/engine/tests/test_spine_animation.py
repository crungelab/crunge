from crunge.engine.loader.spine.spine_json import SpineSkeletonFile

#TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-pro.json"
TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-ess.json"


def test_spine_animation():
    raw = SpineSkeletonFile.load(TEST_FILE)
    #print(raw)

    walk = raw.animations["walk"]
    print("front-thigh rotate keyframes:", walk.bones.get("front-thigh", None) and walk.bones["front-thigh"].rotate)
    print("ik constraints in walk animation:", walk.ik)
    print("ik constraints defined on skeleton:", raw.ik)
