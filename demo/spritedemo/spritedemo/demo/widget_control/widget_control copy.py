from loguru import logger
import glm

from crunge import imgui

from crunge.engine import compose
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.control_2d import Control2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine import Color, colors
from crunge.engine import Renderer
from crunge.engine.ui.button import Button

from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01


class WidgetControl(Control2D):
    def _create(self):
        super()._create()
        self.button = Button("Click Me")
        self.button.layout.set_size(100, 50)

    def _enable(self):
        super()._enable()
        self.button.enable()
        self.button.layout.calculate()
        self.button.layout.apply()
        logger.debug("Button size: {}", self.button.size)

    def _disable(self):
        super()._disable()
        self.button.disable()

    def _draw(self):
        #super()._draw()
        self.button.draw()
        Renderer.get_current().easel.submit_canvas()
        super()._draw()

    def _update(self, delta_time):
        self.button.update(delta_time)
        super()._update(delta_time)

class WidgetControlDemo(Demo):
    def setup(self):
        super().setup()

        self.rotation = 0
        self.scale = 1.0
        self.color = colors.WHITE

        sprite = self.sprite = SpriteLoader().load("${images}/playerShip1_orange.png")

        self.node = WidgetControl(model=sprite).seat(SpriteVu())
        self.scene.attach(self.node)

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None

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

        changed, color = imgui.color_edit4("Tint", self.color)
        if changed:
            self.color = color
            self.sprite.color = color

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
