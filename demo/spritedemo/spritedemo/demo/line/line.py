from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine.d2.line_2d import Line2D
from crunge.engine.d2.node_2d import Node2D


class LineDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def kill(self):
        self.node.destroy()
        self.node = None
        
    def reset(self):
        self.angle = 0
        self.scale = 1.0
        self.color = 1.0, 1.0, 1.0, 1.0

        self.scene.clear()

        sprite = self.sprite = Line2D(glm.vec2(0, 0), glm.vec2(100, 100))
        node = self.node = Node2D(vu=sprite)
        x = self.width / 2
        y = self.height / 2
        node.position = glm.vec2(x, y)

        self.scene.root.attach(self.node)



    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

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

        changed, self.color = imgui.color_edit4("Color", self.color)
        if changed:
            self.sprite.color = glm.vec4(self.color)


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

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super().draw(renderer)

def main():
    LineDemo().create().run()


if __name__ == "__main__":
    main()