from pathlib import Path

from loguru import logger
import glm

from crunge import imgui

from crunge.engine import App, Renderer, Scheduler
from crunge.engine.d2.camera_2d import Camera2D

from crunge.engine.resource.resource_manager import ResourceManager

from crunge.engine.ai.bt.run.task import Runner

from .game_view import GameView
from .game_scene import GameScene


class Game(App):
    """Main application class."""

    view: GameView

    def __init__(self):
        super().__init__(title="Wyggles", resizable=True)

        self.resource_root = Path(__file__).parent / "resources"

        ResourceManager().add_path_variables(
            resources=self.resource_root,
            images=self.resource_root / "images",
        )

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.draw_time = 0
        self.processing_time = 0

        self.debug_agents = False

    def reset(self):
        self.scene = GameScene("default")
        self.create_view()

    def on_display(self):
        super().on_display()

        gui = self.display.gui # initialize the GUI overlay

    @property
    def camera(self) -> Camera2D:
        return self.display.camera

    def create_view(self):
        logger.debug("Creating view")
        self.display = GameView(self.scene)
        self.center_camera()

    def center_camera(self):
        if self.camera:
            ppu = self.camera.ppu
            view_width_units = self.viewport.width / ppu
            view_height_units = self.viewport.height / ppu
            self.camera.position = glm.vec2(view_width_units / 2, view_height_units / 2)
            logger.debug(f"Camera centered at {self.camera.position}")

    def on_size(self):
        super().on_size()
        self.center_camera()

    def _draw(self):
        imgui.begin("Wyggles")

        imgui.text(f"Update time: {self.update_time:.3f}")
        imgui.text(f"Frame time: {self.frame_time:.3f}")

        _, self.debug_agents = imgui.checkbox("Agent Debug Draw", self.debug_agents)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        if self.debug_agents:
            self._draw_debug_agents()

        super()._draw()

    def _draw_debug_agents(self):
        for wyggle in self.scene.wyggle_layer:
            brain = wyggle.brain
            if not brain:
                continue
            txt = brain.state
            position = wyggle.position
            text_offset = glm.vec2(0, 0.5)
            self.display.scratch.draw_text(
                txt, position + text_offset, font_size=12
            )
            """
            focus = brain.focus
            if not focus:
                continue

            self.display.scratch.draw_line(wyggle.position, focus.position)
            """
            target_position = brain.target_position
            self.display.scratch.draw_segment(
                position, target_position
            )


def step_runner(delta_time: float):
    Runner().step()


Scheduler().schedule(step_runner, 0.25)

if __name__ == "__main__":
    Game().run()
