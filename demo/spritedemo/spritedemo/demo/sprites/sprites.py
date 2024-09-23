from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture_loader import TextureLoader


class SpritesDemo(Demo):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1
        # Ship1
        texture = TextureLoader().load(":images:/playerShip1_orange.png")
        sprite = self.sprite = Sprite(texture)
        node = self.node = Node2D(vu=sprite)
        x = self.width / 4
        y = self.height / 4
        node.position = glm.vec2(x, y)
        node.angle = 45
        node.size = glm.vec2(200, 200)

        self.scene.root.attach(self.node)

        # Ship2
        texture = TextureLoader().load(":images:/playerShip1_blue.png")
        sprite = self.sprite = Sprite(texture)
        node = self.node = Node2D(vu=sprite)
        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)
        node.angle = 45
        node.size = glm.vec2(200, 200)

        self.scene.root.attach(self.node)

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

        #TODO: Implement alpha and color
        '''
        # Alpha
        changed, self.alpha = imgui.drag_int("Alpha", self.alpha, 1, 0, 255)
        self.sprite.alpha = self.alpha

        # Color
        _, self.color_enabled = imgui.checkbox("Tint", self.color_enabled)
        if self.color_enabled:
            changed, self.color = imgui.color_edit3("Color", *self.color)
            self.sprite.color = (
                int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255),
            )
        else:
            self.sprite.color = 255, 255, 255
        '''

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

def main():
    SpritesDemo().create().run()


if __name__ == "__main__":
    main()
