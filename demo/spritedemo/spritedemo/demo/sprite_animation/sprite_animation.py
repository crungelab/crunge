from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.color import Color
from crunge.engine.d2.sprite import Sprite, SpriteVu, SpriteAnimation, SpriteAnimationFrame, SpriteAnimator
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader


class SpriteAnimationDemo(Demo):
    def __init__(self):
        super().__init__()

    def create(self):
        super().create()
        self.reset()
        return self

    def kill(self):
        self.node.destroy()
        self.node = None
        
    def reset(self):
        self.angle = 0
        self.scale = 1.0

        self.scene.clear()

        atlas = self.atlas = XmlSpriteAtlasLoader().load(
            ":resources:/characters/robot/sheet.xml"
        )
        logger.debug(f"atlas: {atlas}")

        sprite = self.sprite = atlas.get("idle")


        node = self.node = Node2D(vu=SpriteVu(), model=sprite)

        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)

        self.scene.attach(self.node)

        animator = self.animator = SpriteAnimator(node)
        self.create_animations()
        animator.play("walkRight")

    def create_animations(self):
        self.create_walk_animations()
        self.create_run_animations()

    def create_walk_animations(self):
        atlas = self.atlas
        animator = self.animator
        
        walk_right = SpriteAnimation("walkRight")
        for i in range(0, 8):
            frame = SpriteAnimationFrame(atlas.get(f"walk{i}"))
            walk_right.add_frame(frame)

        animator.add_animation(walk_right)

        walk_left = walk_right.mirror("walkLeft", horizontal=True)

        animator.add_animation(walk_left)

    def create_run_animations(self):
        atlas = self.atlas
        animator = self.animator

        run_right = SpriteAnimation("runRight")
        for i in range(0, 3):
            frame = SpriteAnimationFrame(atlas.get(f"run{i}"))
            run_right.add_frame(frame)

        animator.add_animation(run_right)

        run_left = run_right.mirror("runLeft", horizontal=True)

        animator.add_animation(run_left)

    def update(self, delta_time):
        #logger.debug(f"Update: {delta_time}")
        self.animator.update(delta_time)
        return super().update(delta_time)

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Sprite Animation")

        if imgui.button("Reset"):
            self.reset()

        # Rotation
        changed, self.angle = imgui.drag_float(
            "Angle",
            self.angle,
        )
        if changed:
            self.node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        if changed:
            self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.begin_list_box("Animations"):

            for name, animation in self.animator.animations.items():
                opened, selected = imgui.selectable(name, animation == self.animator.current_animation)
                if opened:
                    logger.debug(f"Selected: {name}")
                    self.animator.play(name)

            imgui.end_list_box()

        imgui.end()

        super().draw(renderer)

def main():
    SpriteAnimationDemo().create().run()


if __name__ == "__main__":
    main()
