from pathlib import Path

from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from crunge.engine import Color, colors
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.shape.circle_2d import Circle2D


class CircleDemo(Demo):
    def reset(self):
        self.angle = 0
        self.scale = 1.0
        self.color = colors.WHITE

        self.scene.clear()

        shape = self.shape = Circle2D(
            glm.vec2(0, 0), radius=100.0, segments=32, color=self.color
        )
        self.node = Node2D(vu=shape)
        self.scene.attach(self.node)

    def kill(self):
        self.node.destroy()
        self.node = None

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Circle")

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
    CircleDemo().run()


if __name__ == "__main__":
    main()
