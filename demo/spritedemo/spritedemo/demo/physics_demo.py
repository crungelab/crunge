from crunge import imgui

from crunge.engine.d2.physics.draw_options import DrawOptions
from crunge.engine.d2.physics import DynamicPhysicsEngine

from .demo import Demo


class PhysicsDemo(Demo):
    def reset(self):
        super().reset()

        self.debug_draw_enabled = False
        self.draw_options = DrawOptions(self.view.scratch)

        self.physics_engine = DynamicPhysicsEngine().create()

    def _draw(self):
        if self.debug_draw_enabled:
            self.physics_engine.debug_draw(self.draw_options)

        super()._draw()

    def draw_physics_options(self):
        _, self.debug_draw_enabled = imgui.checkbox(
            "Debug Draw", self.debug_draw_enabled
        )
