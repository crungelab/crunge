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


def _mat3_translation(m: glm.mat3) -> glm.vec2:
    # translation lives in column 2 per compose_local's constructor layout
    return glm.vec2(m[2][0], m[2][1])


class AnimationPage(Page):
    def reset(self):
        super().reset()

        self.angle = 0
        self.scale = 1.0
        self.selected_slot_index = None
        self.paused = False

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

        changed, self.angle = imgui.drag_float("Angle", self.angle, 0.1)
        if changed:
            self.node.angle = self.angle

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

        if imgui.begin_list_box("Skins"):
            for name, skin in self.skeleton.data.skins.items():
                opened, selected = imgui.selectable(
                    name, name == self.skeleton.current_skin_name
                )
                if opened:
                    logger.debug(f"Selected skin: {name}")
                    self.skeleton.set_skin(name)
            imgui.end_list_box()

        if imgui.button("Reset"):
            self.window.reshow_channel()

        imgui.end()

        self._draw_debug_panel()

        super()._draw()

    def _draw_debug_panel(self):
        imgui.begin("Spine Debug")

        entry = self.anim_state.current
        if entry is not None:
            imgui.text(
                f"anim: {entry.animation.name}  "
                f"t={entry.time:.3f} / {entry.animation.duration:.3f}  "
                f"timelines={len(entry.animation.timelines)}"
            )
        else:
            imgui.text("anim: (none playing)")

        _, self.paused = imgui.checkbox("Pause", self.paused)
        if self.paused and entry is not None:
            imgui.same_line()
            changed, entry.time = imgui.drag_float("Time", entry.time, 0.01)

        imgui.separator()
        imgui.text("Slots (name / attachment / sprite / bone xy)")

        if imgui.begin_list_box("##slots", (-1, 220)):
            for i, slot in enumerate(self.skeleton.slots):
                att = slot.attachment
                att_name = att.path if att is not None else "-"
                has_sprite = (
                    "Y"
                    if (
                        att is not None
                        and (att.gpu_sprite is not None or att.sequence_sprites)
                    )
                    else "N"
                )
                pos = _mat3_translation(slot.bone.world)
                label = f"{i:2d} {slot.data.name:20s} {att_name:20s} sprite={has_sprite} bone=({pos.x:.2f},{pos.y:.2f})"
                opened, _ = imgui.selectable(label, self.selected_slot_index == i)
                if opened:
                    self.selected_slot_index = i
            imgui.end_list_box()

        imgui.separator()

        if self.selected_slot_index is not None:
            self._draw_slot_details(self.selected_slot_index)

        imgui.end()

    def _draw_slot_details(self, slot_index: int):
        slot = self.skeleton.slots[slot_index]
        bone = slot.bone
        att = slot.attachment

        imgui.text(f"slot: {slot.data.name}  (index {slot_index})")
        imgui.text(f"bone: {bone.data.name}  (setup rotation={bone.data.rotation:.2f})")
        imgui.text(f"bone.rotation (live pose): {bone.rotation:.2f}")

        pos = _mat3_translation(bone.world)
        imgui.text(f"bone.world translation: ({pos.x:.4f}, {pos.y:.4f})")

        if att is not None:
            imgui.text(
                f"attachment: {att.path}  "
                f"xy=({att.x:.3f},{att.y:.3f}) rot={att.rotation:.2f} "
                f"size=({att.width:.3f},{att.height:.3f})"
            )
            if att.sequence is not None:
                imgui.text(
                    f"sequence: count={att.sequence.count} "
                    f"digits={att.sequence.digits} "
                    f"frame={slot.sequence_index} "
                    f"resolved={sum(s is not None for s in att.sequence_sprites)}/{len(att.sequence_sprites)}"
                )
        else:
            imgui.text("attachment: (none)")

        imgui.separator()
        imgui.text("Which timelines in the current animation target this slot/bone:")

        bone_index = self.skeleton.bones.index(bone)
        entry = self.anim_state.current
        if entry is not None:
            hits = [
                type(tl).__name__
                for tl in entry.animation.timelines
                if getattr(tl, "bone_index", None) == bone_index
                or getattr(tl, "slot_index", None) == slot_index
            ]
            imgui.text(
                ", ".join(hits)
                if hits
                else "(none — this is why it may look static/hidden)"
            )

        imgui.separator()
        imgui.text("Animations with a timeline for this bone/slot:")
        for name, anim in self.skeleton.data.animations.items():
            hits = [
                type(tl).__name__
                for tl in anim.timelines
                if getattr(tl, "bone_index", None) == bone_index
                or getattr(tl, "slot_index", None) == slot_index
            ]
            if hits:
                imgui.text(f"  {name}: {', '.join(hits)}")

    def update(self, delta_time):
        if not self.paused:
            self.anim_state.update(delta_time)
        self.anim_state.apply()
        self.skeleton_vu.update_pose()
        return super().update(delta_time)


def install(app: App):
    app.add_channel(SpineEssChannel(AnimationPage, "alien", "Alien"))
    app.add_channel(SpineEssChannel(AnimationPage, "dragon", "Dragon"))
    app.add_channel(SpineEssChannel(AnimationPage, "goblins", "Goblins"))
    app.add_channel(SpineEssChannel(AnimationPage, "hero", "Hero"))
    app.add_channel(SpineEssChannel(AnimationPage, "powerup", "Powerup"))
    app.add_channel(SpineEssChannel(AnimationPage, "speedy", "Speedy"))
    app.add_channel(SpineEssChannel(AnimationPage, "windmill", "Windmill"))
