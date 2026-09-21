from loguru import logger
import glm

from crunge import imgui
from crunge import yoga


from crunge.engine.d2.control import WidgetControl2D
from crunge.engine.ui.button import Button


from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01
ZOOM_STEP = 0.01


class WidgetControlDemo(Demo):
    def setup(self):
        super().setup()

        self.rotation = 0
        self.scale = 1.0
        self.zoom = 1.0

        self.button = Button(
            "Hello, World!",
            on_click=self.on_click,
            style=yoga.StyleBuilder().size(200, 50).build(),
        )

        self.node = WidgetControl2D(self.button)
        self.scene.attach(self.node)

    def on_click(self):
        logger.info(f"Button clicked: {self.button.text}")

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Widget Control")

        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        if changed and self.node is not None:
            self.node.rotation = self.rotation

        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        if changed and self.node is not None:
            self.node.scale = glm.vec2(self.scale, self.scale)

        changed, self.zoom = imgui.drag_float("Zoom", self.zoom, ZOOM_STEP)
        if changed and self.node is not None:
            self.camera.zoom = self.zoom

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super()._draw()


def main():
    WidgetControlDemo().run()


if __name__ == "__main__":
    main()
