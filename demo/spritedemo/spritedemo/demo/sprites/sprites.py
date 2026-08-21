from loguru import logger
import glm

from crunge import imgui

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader

from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01


class SpritesDemo(Demo):

    def reset(self):
        super().reset()

        self.rotation = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

        # Ship1
        sprite = SpriteLoader().load("${images}/playerShip1_orange.png")

        node = self.node = Node2D(vu=SpriteVu(), model=sprite)

        self.scene.attach(self.node)

        # Ship2
        sprite = SpriteLoader().load("${images}/playerShip1_blue.png")
        x = 1.0
        y = 1.0

        position = glm.vec2(x, y)
        node = Node2D(position, vu=SpriteVu(), model=sprite)

        self.scene.attach(node)

    def center_camera(self):
        pass

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Ship")

        # Rotation
        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        if changed:
            self.node.rotation = self.rotation

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        if changed:
            self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()


def main():
    SpritesDemo().run()


if __name__ == "__main__":
    main()
