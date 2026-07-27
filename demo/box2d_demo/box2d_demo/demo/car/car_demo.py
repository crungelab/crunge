from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.settings_2d import Settings2D

from ..physics_demo import PhysicsDemo

from .floor import Floor

from ...characters import Skateboard


class CarDemo(PhysicsDemo):
    def reset(self):
        super().reset()
        self.create_floor()
        self.create_avatar(glm.vec2(3, 3))

    # ------------------------------------------------------------------
    # Input — extend base drag behaviour with box creation
    # ------------------------------------------------------------------

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)  # right-click drag handled here
        if event.button == 1 and event.down:
            world = self.camera.unproject(glm.vec2(event.x, event.y))
            logger.debug(f"Creating box at {world}")
            self.create_box(world)

    # ------------------------------------------------------------------
    # Scene helpers
    # ------------------------------------------------------------------

    def create_box(self, position):
        self.scene.attach(Box(position))

    def create_floor(self):
        ppu = Settings2D().ppu
        width_units = self.width / ppu  # viewport width, converted to units
        x = width_units / 2
        y = 0
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(width_units * 5, 2))  # 2 units thick, not 2 px
        floor.create()
        self.scene.attach(floor)

    def create_avatar(self, position):
        self.push_avatar(Skateboard(position))
        self.scene.attach(self.avatar)

    # ------------------------------------------------------------------
    # UI & update
    # ------------------------------------------------------------------

    def _draw(self):
        imgui.begin("Skateboard Demo")
        imgui.text("Click empty space to create boxes")
        imgui.text("Click & drag boxes to move them")

        self.draw_stats()
        self.draw_physics_options()

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super()._draw()


def main():
    CarDemo().run()


if __name__ == "__main__":
    main()
