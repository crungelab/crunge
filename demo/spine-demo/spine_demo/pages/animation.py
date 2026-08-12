from loguru import logger
import glm

from crunge import imgui

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.skeleton.animation import AnimationState

from crunge.engine.loader.spine.spine_skeleton_loader import SpineSkeletonLoader
from crunge.engine.d2.skeleton.skeleton_vu import SkeletonVu

from crunge.engine import App

from ..channel import SpineEssChannel, SpineProChannel

from ..page import Page


class AnimationPage(Page):
    def reset(self):
        super().reset()

        self.angle = 0
        self.scale = 1.0

        loader = SpineSkeletonLoader()
        name = self.name
        version = self.version
        path = f":spines:/{name}/export/{name}-{version}.json"
        skeleton = loader.load(path, f"{name}.atlas")

        self.anim_state = AnimationState(skeleton)
        first_anim_name = next(iter(skeleton.data.animations))
        self.current_animation = skeleton.data.animations[first_anim_name]
        self.anim_state.set_animation(self.current_animation)
        self.skeleton = skeleton
        self.skeleton_vu = SkeletonVu(skeleton)
        self.node = Node2D(vu=self.skeleton_vu)
        self.scene.attach(self.node)

    def _draw(self):
        imgui.begin("Properties")

        # Rotation
        changed, self.angle = imgui.drag_float("Angle", self.angle, 0.1)
        if changed:
            self.node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        if changed:
            self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.begin_list_box("Animations"):

            for name, animation in self.skeleton.data.animations.items():
                opened, selected = imgui.selectable(
                    name, animation == self.current_animation
                )
                if opened:
                    logger.debug(f"Selected: {name}")
                    self.current_animation = self.skeleton.data.animations[name]
                    self.anim_state.set_animation(self.current_animation)

            imgui.end_list_box()

        if imgui.button("Reset"):
            self.window.reshow_channel()

        imgui.end()

        super()._draw()

    def update(self, delta_time):
        self.anim_state.update(delta_time)
        self.anim_state.apply()  # this now does set_to_setup_pose + timelines + update_world_transforms
        self.skeleton_vu.update_pose()  # pushes the freshly-computed bone.world into each slot_vu.transform
        return super().update(delta_time)


def install(app: App):
    app.add_channel(SpineEssChannel(AnimationPage, "alien", "Alien"))
    app.add_channel(SpineEssChannel(AnimationPage, "dragon", "Dragon"))
    app.add_channel(SpineEssChannel(AnimationPage, "goblins", "Goblins"))
    app.add_channel(SpineEssChannel(AnimationPage, "hero", "Hero"))
    app.add_channel(SpineEssChannel(AnimationPage, "powerup", "Powerup"))
    app.add_channel(SpineEssChannel(AnimationPage, "speedy", "Speedy"))
    #app.add_channel(SpineEssChannel(AnimationPage, "spinosaurus", "Spinosaurus"))
    app.add_channel(SpineEssChannel(AnimationPage, "windmill", "Windmill"))

    #app.add_channel(SpineProChannel(AnimationPage, "owl", "Owl"))

'''
def install(app: App):
    app.add_channel(SpineDemoChannel(AnimationPage, "hero", "Hero"))
    #app.add_channel(SpineDemoChannel(AnimationPage, "owl", "Owl"))
    app.add_channel(SpineDemoChannel(AnimationPage, "alien", "Alien"))
'''