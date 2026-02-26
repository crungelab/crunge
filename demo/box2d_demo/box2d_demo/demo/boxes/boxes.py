from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from ..physics_demo import PhysicsDemo

from .box import Box
from .floor import Floor


class BoxesDemo(PhysicsDemo):
    def reset(self):
        super().reset()
        self.create_floor()

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
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(self.width, 20))
        floor.create()
        self.scene.attach(floor)

    # ------------------------------------------------------------------
    # UI & update
    # ------------------------------------------------------------------

    def _draw(self):
        imgui.begin("Boxes Demo")
        imgui.text("Click empty space to create boxes")
        imgui.text("Click & drag boxes to move them")

        self.draw_stats()
        self.draw_physics_options()

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super()._draw()

    def update(self, delta_time: float):
        self.world.update(1 / 60)
        self.scene.update(delta_time)
        super().update(delta_time)


def main():
    BoxesDemo().run()


if __name__ == "__main__":
    main()
