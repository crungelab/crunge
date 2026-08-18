from crunge.engine.loader.spine.spine_converter import load_skeleton_data
from crunge.engine.d2.skeleton import Skeleton, AnimationState

#TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-pro.json"
from . import resolve_spine_path

def test_spine_skeleton():
    path = resolve_spine_path("spineboy", ext="json")
    skel_data = load_skeleton_data(path)
    skeleton = Skeleton(skel_data)
    anim_state = AnimationState(skeleton)

    # pick a real animation name from your file
    first_anim_name = next(iter(skel_data.animations))
    anim_state.set_animation(skel_data.animations[first_anim_name])

    skeleton.set_to_setup_pose()
    skeleton.update_world_transforms()
    print("setup pose root world:", skeleton.bones[0].world)

    for step in range(5):
        anim_state.update(1.0 / 30.0)
        anim_state.apply()
        b = skeleton.bones[-1]  # last bone, arbitrary — pick one you know moves
        print(
            f"t={anim_state.current.time:.3f}  pos=({b.x:.3f}, {b.y:.3f})  rot={b.rotation:.2f}"
        )
