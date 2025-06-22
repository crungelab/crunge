from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader


class SpritesDemo(Demo):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

    def intro(self):
        super().intro()
        # Ship1
        texture = ImageTextureLoader().load(":images:/playerShip1_orange.png")
        sprite = Sprite(texture)
        x = self.width / 4
        y = self.height / 4
        position = glm.vec2(x, y)
        node = self.node = Node2D(position, vu=SpriteVu(), model=sprite)
        node.angle = 45

        self.scene.attach(self.node)

        # Ship2
        texture = ImageTextureLoader().load(":images:/playerShip1_blue.png")
        sprite = Sprite(texture)
        x = self.width / 2
        y = self.height / 2
        position = glm.vec2(x, y)
        node = self.node = Node2D(position, vu=SpriteVu(), model=sprite)
        node.angle = 45

        self.scene.attach(self.node)

    def on_size(self):
        super().on_size()
        self.center_camera()

    def reset(self):
        self.angle = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Ship")

        # Rotation
        changed, self.angle = imgui.drag_float(
            "Angle",
            self.angle,
        )
        self.node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)


def main():
    SpritesDemo().create().run()


if __name__ == "__main__":
    main()
