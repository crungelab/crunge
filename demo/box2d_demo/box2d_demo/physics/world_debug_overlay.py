from loguru import logger

from .debug_draw import DebugDraw

from crunge import skia

from crunge.engine.renderer import Renderer
from crunge.engine.widget import Overlay

from .world import PhysicsWorld2D

class WorldDebugOverlay(Overlay):
    def __init__(self):
        super().__init__("world_debug", 700)
        self.visible = False
        self.debug_draw = DebugDraw()

    def _draw(self):
        world = PhysicsWorld2D.get_current()

        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            canvas.save()

            canvas.translate(renderer.viewport.width // 2, renderer.viewport.height // 2)
            scale = 1 / renderer.camera_2d.zoom
            canvas.scale(scale, -scale)  # Invert Y-axis for Skia
            camera_x, camera_y = (
                renderer.camera_2d.position.x,
                renderer.camera_2d.position.y,
            )
            canvas.translate(-camera_x, -camera_y)  # pan to camera

            world.draw(self.debug_draw)

            canvas.restore()

        super()._draw()
