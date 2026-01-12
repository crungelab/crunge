from pathlib import Path

from loguru import logger
import glm

from crunge import imgui

from ..demo import Demo
from crunge.engine.d2.background import BackgroundVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite.background_sprite_builder import BackgroundSpriteBuilder
from crunge.engine.color import Color
from crunge.engine import colors


class BackgroundDemo(Demo):        
    def reset(self):
        super().reset()
        
        self.angle = 0
        self.scale = 1.0
        self.color = colors.WHITE

        sprite = self.sprite = SpriteLoader(sprite_builder=BackgroundSpriteBuilder()).load(":images:/backgroundColorGrass.png")
        self.node = Node2D(vu=BackgroundVu(), model=sprite)
        self.scene.attach(self.node)

    def kill(self):
        self.node.destroy()
        self.node = None

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Background")

        '''
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
        '''

        # Tint
        changed, color = imgui.color_edit4("Tint", self.color)
        if changed:
            self.color = color
            self.sprite.color = color

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super()._draw()

def main():
    BackgroundDemo().run()


if __name__ == "__main__":
    main()
