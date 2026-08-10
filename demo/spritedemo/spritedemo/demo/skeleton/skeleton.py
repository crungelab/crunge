from loguru import logger
import glm

from crunge import imgui

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine import Color, colors
from crunge.engine.d2.skeleton.animation import AnimationState
from ..demo import Demo

from crunge.engine.loader.spine.spine_skeleton_loader import SpineSkeletonLoader
from crunge.engine.d2.skeleton.skeleton_vu import SkeletonVu

#TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-pro.json"
TEST_FILE = "/home/kurt/Dev/crunge/depot/spineboy-4.3/export/spineboy-ess.json"


class SpriteDemo(Demo):
    def reset(self):
        super().reset()

        self.angle = 0
        self.scale = 1.0

        loader = SpineSkeletonLoader()
        skeleton = loader.load(TEST_FILE, "spineboy.atlas")

        skeleton.set_to_setup_pose()
        skeleton.update_world_transforms()
        self.anim_state = AnimationState(skeleton)
        first_anim_name = next(iter(skeleton.data.animations))
        #self.anim_state.set_animation(skeleton.data.animations[first_anim_name])
        self.anim_state.set_animation(skeleton.data.animations["walk"])

        head_slot = next(s for s in skeleton.slots if s.data.name == "head")
        print("attachment:", head_slot.attachment)
        print("gpu_sprite:", head_slot.attachment.gpu_sprite if head_slot.attachment else None)
        print("bone world:", head_slot.bone.world)

        print("skins available:", list(skeleton.data.skins.keys()))
        print("current skin name:", skeleton.current_skin_name)
        print("attachments in current skin:", list(skeleton.data.skins[skeleton.current_skin_name].keys()))
        print("all slot names:", [s.data.name for s in skeleton.slots])

        bone = next(b for b in skeleton.bones if b.data.name == "front-thigh")

        self.anim_state.update(0.5)  # jump partway into the walk cycle
        self.anim_state.apply()

        print("bone.rotation (pose field):", bone.rotation)
        print("bone.local:", bone.local)
        print("bone.world:", bone.world)

        #exit()

        self.skeleton_vu = SkeletonVu(skeleton)
        self.node = Node2D(vu=self.skeleton_vu)
        self.scene.attach(self.node)

    def center_camera(self):
        pass

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Ship")

        # Rotation
        changed, self.angle = imgui.drag_float("Angle", self.angle, 0.1)
        if changed:
            self.node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        if changed:
            self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()

    def update(self, delta_time):
        self.anim_state.update(delta_time)
        self.anim_state.apply()          # this now does set_to_setup_pose + timelines + update_world_transforms
        self.skeleton_vu.update_pose()   # pushes the freshly-computed bone.world into each slot_vu.transform
        return super().update(delta_time)

    '''
    def update(self, delta_time):
        self.skeleton_vu.update_pose()
        return super().update(delta_time)
    '''

def main():
    SpriteDemo().run()


if __name__ == "__main__":
    main()
