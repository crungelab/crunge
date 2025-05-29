from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.sprite.group.instanced_sprite_vu_group import InstancedSpriteVuGroup

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.color import Color

INITIAL_SCALE = 0.5

class InstancingDemo(Demo):
    def __init__(self):
        super().__init__()
        self.nodes: list[Node2D] = []
        texture = ImageTextureLoader().load(":images:/playerShip1_orange.png")
        self.color = tuple(Color.WHITE.value)
        self.sprite = Sprite(texture, color=glm.vec4(self.color))

    def create(self):
        super().create()
        self.reset()
        return self

    def kill(self):
        for node in self.nodes:
            node.destroy()
        self.nodes.clear()
        
    def reset(self):
        self.sprite_vu_group = InstancedSpriteVuGroup(1024)

        self.angle = 0
        self.scale = INITIAL_SCALE
        #self.color = 1.0, 1.0, 1.0, 1.0
        self.color = tuple(Color.WHITE.value)

        self.scene.clear()

        self.create_sprites()


    def create_sprites(self):
        # Set grid size and spacing
        grid_size = 10
        spacing = 64  # Adjust spacing between sprites as needed

        for row in range(grid_size):
            for col in range(grid_size):
                vu = SpriteVu(self.sprite).config(group=self.sprite_vu_group)
                node = Node2D(vu=vu).config(scale=glm.vec2(self.scale, self.scale))
                
                # Calculate position based on grid and spacing
                x = col * spacing - (grid_size * spacing) / 2 + self.width / 2
                y = row * spacing - (grid_size * spacing) / 2 + self.height / 2
                
                node.position = glm.vec2(x, y)
                self.nodes.append(node)
                self.scene.attach(node)

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
            for node in self.nodes:
                node.angle = self.angle

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        if changed:
            for node in self.nodes:
                node.scale = glm.vec2(self.scale, self.scale)

        changed, self.color = imgui.color_edit4("Tint", self.color)
        if changed:
            self.sprite.color = glm.vec4(self.color)

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super().draw(renderer)

        with self.view.renderer as renderer:
            self.sprite_vu_group.draw(renderer)


def main():
    InstancingDemo().create().run()


if __name__ == "__main__":
    main()
