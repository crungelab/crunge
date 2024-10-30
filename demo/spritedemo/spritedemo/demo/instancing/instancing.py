from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite, SpriteMaterial
from crunge.engine.d2.sprite.render_group.sprite_render_group import SpriteRenderGroup

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture_loader import TextureLoader
from crunge.engine.color import Color


class InstancingDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def kill(self):
        self.node.destroy()
        self.node = None
        
    def reset(self):
        self.render_group = SpriteRenderGroup()

        self.angle = 0
        self.scale = 1.0
        #self.color = 1.0, 1.0, 1.0, 1.0
        self.color = tuple(Color.WHITE.value)

        self.scene.clear()

        texture = TextureLoader().load(":images:/playerShip1_orange.png")
        material = SpriteMaterial(texture, color=glm.vec4(self.color))
        #sprite = self.sprite = Sprite(material).create()
        sprite = self.sprite = Sprite(material).create(self.render_group)
        node = self.node = Node2D(vu=sprite)
        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)

        self.scene.root.attach(self.node)



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
            self.sprite.material.color = glm.vec4(self.color)

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        #self.render_group.draw(renderer)
        self.render_group.draw(self.view.renderer)

        super().draw(renderer)

def main():
    InstancingDemo().create().run()


if __name__ == "__main__":
    main()
