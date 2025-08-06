from loguru import logger
import glm

from crunge import imgui

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite, SpriteVu

from crunge.engine.d2.sprite.instanced import InstancedSpriteLayer

from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine import colors

INITIAL_SCALE = 0.5


class InstancingDemo(Demo):
    def __init__(self):
        super().__init__()
        self.nodes: list[Node2D] = []
        self.color = colors.WHITE

    def create_scene(self):
        super().create_scene()
        self.sprite_group = DynamicSpriteGroup(1024)
        layer = InstancedSpriteLayer("sprites", 1024, self.sprite_group)
        self.scene.add_layer(layer)
        texture = ImageTextureLoader().load(":images:/playerShip1_orange.png")
        self.sprite = Sprite(texture, color=self.color)

    def reset(self):
        super().reset()

        self.nodes.clear()
        self.color = colors.WHITE
        self.sprite.color = self.color
        self.angle = 0
        self.scale = INITIAL_SCALE

        # Set grid size and spacing
        grid_size = 10
        spacing = 64  # Adjust spacing between sprites as needed

        for row in range(grid_size):
            for col in range(grid_size):
                vu = SpriteVu(self.sprite)
                node = Node2D(scale=glm.vec2(self.scale, self.scale), vu=vu)

                # Calculate position based on grid and spacing
                x = col * spacing - (grid_size * spacing) / 2 + self.width / 2
                y = row * spacing - (grid_size * spacing) / 2 + self.height / 2

                node.position = glm.vec2(x, y)
                self.nodes.append(node)
                self.scene.attach(node)

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Instancing")

        # Rotation
        changed, self.angle = imgui.drag_float(
            "Angle",
            self.angle,
        )
        if changed:
            for node in self.nodes:
                node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        if changed:
            for node in self.nodes:
                node.scale = glm.vec2(self.scale, self.scale)

        changed, color = imgui.color_edit4("Tint", self.color)

        if changed:
            self.color = color
            self.sprite.color = color

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()


def main():
    InstancingDemo().run()


if __name__ == "__main__":
    main()
