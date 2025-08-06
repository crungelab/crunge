from loguru import logger
import glm

from crunge import imgui
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.sprite_array_loader import SpriteArrayLoader
from crunge.engine.resource.resource_manager import ResourceManager

from ..demo import Demo


class SpriteArrayDemo(Demo):
    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()

        self.angle = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

        folder = ResourceManager().resolve_path(":resources:/tiled/items/")
        logger.debug(f"folder: {folder}")

        paths = list(folder.glob("*.png"))
        logger.debug(f"paths: {paths}")

        atlas = self.atlas = SpriteArrayLoader().load(paths)
        logger.debug(f"atlas: {atlas}")

        sprite = self.sprite = atlas.get("bomb.png")

        # self.sprite_vu = vu = SpriteVu(sprite).create()
        # node = self.node = Node2D(vu=vu)
        self.sprite_vu = vu = SpriteVu()
        node = self.node = Node2D(vu=vu, model=sprite)
        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)

        self.scene.attach(self.node)

    def _draw(self):
        # imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Object")

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

        imgui.begin("Textures")

        if imgui.begin_list_box("Textures", (-1, -1)):

            for name, sprite in self.atlas.sprite_map.items():
                # opened, selected = imgui.selectable(name, texture == self.texture)
                opened, selected = imgui.selectable(name, sprite == self.sprite)
                if opened:
                    logger.debug(f"Selected: {name}")
                    # self.texture = texture

                    self.sprite = sprite
                    self.sprite_vu.sprite = sprite

            imgui.end_list_box()

        imgui.end()

        super()._draw()


def main():
    SpriteArrayDemo().run()


if __name__ == "__main__":
    main()
