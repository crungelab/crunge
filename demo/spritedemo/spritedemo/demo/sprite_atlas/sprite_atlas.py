from loguru import logger
import glm

from crunge import imgui

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01


class SpriteAtlasDemo(Demo):
    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()

        self.rotation = 0
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

        atlas = self.atlas = XmlSpriteAtlasLoader().load(
            "${resources}/platformer/Spritesheets/spritesheet_tiles.xml"
        )
        logger.debug(f"atlas: {atlas}")

        sprite = self.sprite = atlas.get("bomb.png")

        self.sprite_vu = vu = SpriteVu()
        node = self.node = Node2D(model=sprite).mount(vu)
        x = self.width / 2 / self.ppu
        y = self.height / 2 / self.ppu
        node.position = glm.vec2(x, y)

        self.scene.attach(self.node)

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Object")

        # Rotation
        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        self.node.rotation = self.rotation

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        imgui.begin("Textures")

        if imgui.begin_list_box("##Textures", (-1, -1)):

            for name, sprite in self.atlas.sprite_map.items():
                clicked, selected = imgui.selectable(name, sprite == self.sprite)
                if clicked:
                    logger.debug(f"Selected: {name}")
                    self.sprite = sprite
                    self.sprite_vu.sprite = sprite

            imgui.end_list_box()

        imgui.end()

        super()._draw()


def main():
    SpriteAtlasDemo().run()


if __name__ == "__main__":
    main()
