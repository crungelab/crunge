from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine import Color, colors
from crunge.engine.d2.shape.line_2d import Line2D
from crunge.engine.d2.node_2d import Node2D


class LineDemo(Demo):
    def reset(self):
        super().reset()

        self.angle = 0
        self.scale = 1.0
        self.color = colors.WHITE

        #self.scene.clear()

        shape = self.shape = Line2D(glm.vec2(0, 0), glm.vec2(100, 100))
        self.node = Node2D(vu=shape)
        self.scene.attach(self.node)

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Line")

        # Position
        changed, position = imgui.drag_float2("Position", tuple(self.node.position))
        if changed:
            self.node.position = glm.vec2(position)

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

        changed, color = imgui.color_edit4("Color", self.color)
        if changed:
            self.color = color
            self.shape.color = color

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super().draw(renderer)


def main():
    LineDemo().run()


if __name__ == "__main__":
    main()
