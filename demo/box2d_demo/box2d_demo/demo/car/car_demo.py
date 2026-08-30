from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.settings_2d import Settings2D


from ...objects.floor import Floor
from ...character import Car

from ..physics_demo import PhysicsDemo


class CarDemo(PhysicsDemo):
    def reset(self):
        super().reset()
        self.create_floor()
        self.create_avatar(glm.vec2(3, 3))

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
        self.push_avatar(Car(position))
        self.scene.attach(self.avatar)

    # ------------------------------------------------------------------
    # UI & update
    # ------------------------------------------------------------------

    def _draw(self):
        imgui.begin("Car Demo")
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
