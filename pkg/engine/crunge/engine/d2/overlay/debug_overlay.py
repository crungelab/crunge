from __future__ import annotations
from contextlib import contextmanager

from loguru import logger

from crunge import skia
from crunge.engine.vu import Vu

from ...renderer import Renderer
from ...widget import Overlay


class DebugOverlay(Overlay):
    """Overlay that draws in world-space via the camera's ppu/zoom transform.

    Everything reaching draw_items() is in world units, Y-up: the canvas
    carries the camera transform, including the flip. Do not project to
    screen space before calling — that applies the camera twice.
    """

    def __init__(self, name: str, priority: int = 0, vu: Vu = None) -> None:
        super().__init__(name, priority, vu)
        self.outline_width_px = 1.0  # desired constant on-screen thickness

    @property
    def camera(self):
        return self.display.camera

    @property
    def viewport(self):
        return self.display.viewport

    @property
    def canvas(self) -> skia.Canvas:
        return self.display.renderer.canvas

    @property
    def ppu(self) -> float:
        return self.camera.ppu

    def _camera_scale(self) -> float:
        """World units -> pixels. The single definition of that factor.

        This was previously computed in three places: here, inline in
        world_canvas, and in _scaled_stroke_width against a memoized ppu that
        was never invalidated. The stroke width read a stale ppu against a
        live zoom, so any runtime ppu change silently desynced the outline
        from the canvas it was drawn on.
        """
        camera = self.camera
        return camera.ppu / camera.zoom

    @contextmanager
    def world_canvas(self):
        camera = self.camera
        rect = self.viewport.global_rect
        with self.display.renderer.canvas_target() as canvas:
            canvas.save()
            canvas.translate(
                rect.x + rect.width // 2,
                rect.y + rect.height // 2,
            )
            scale = self._camera_scale()
            canvas.scale(scale, -scale)
            canvas.translate(-camera.position.x, -camera.position.y)
            try:
                yield canvas
            finally:
                canvas.restore()

    def _scaled_stroke_width(self) -> float:
        """World-unit width that renders as outline_width_px on screen."""
        return self.outline_width_px / self._camera_scale()

    def _draw(self):
        with self.world_canvas() as canvas:
            self.draw_items()

    def draw_items(self):
        pass  # Implement in subclasses to draw specific items in world space