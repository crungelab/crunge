from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.color import Color


class SpriteDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def kill(self):
        self.node.destroy()
        self.node = None
        
    def reset(self):
        self.angle = 0
        self.scale = 1.0
        #self.color = 1.0, 1.0, 1.0, 1.0
        self.color = tuple(Color.WHITE.value)

        self.scene.clear()

        texture = ImageTextureLoader().load(":images:/playerShip1_orange.png")
        sprite = self.sprite = Sprite(texture, color=glm.vec4(self.color))
        vu = SpriteVu(sprite).create()
        node = self.node = Node2D(vu=vu)
        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)

        self.scene.attach(self.node)



    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Ship")

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

        changed, self.color = imgui.color_edit4("Tint", self.color)
        if changed:
            self.sprite.color = glm.vec4(self.color)

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super().draw(renderer)

def main():
    SpriteDemo().create().run()


if __name__ == "__main__":
    main()
