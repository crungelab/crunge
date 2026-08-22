from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass

from crunge import skia
from crunge.engine.vu import Vu

from ...renderer import Renderer
from ...widget import Overlay

@dataclass
class DebugOverlayMemo:
    ppu: float
    
class DebugOverlay(Overlay):
    """Overlay that draws in world-space via the camera's ppu/zoom transform."""
    def __init__(self, name: str, priority: int = 0, vu: Vu = None) -> None:
        super().__init__(name, priority, vu)
        self._memo: DebugOverlayMemo = None
        self.outline_width_px = 1.0  # desired constant on-screen thickness

    @property
    def canvas(self) -> skia.Canvas:
        return Renderer.get_current().canvas
    
    @property
    def memo(self):
        if self._memo is None:
            renderer = Renderer.get_current()
            ppu = renderer.camera_2d.ppu
            self._memo = DebugOverlayMemo(ppu=ppu)
        return self._memo

    @property
    def ppu(self) -> float:
        return self.memo.ppu

    """
    @property
    def ppu(self) -> float:
        renderer = Renderer.get_current()
        return renderer.camera_2d.ppu
    """

    def _camera_scale(self) -> float:
        camera = Renderer.get_current().camera_2d
        return camera.ppu / camera.zoom

    @contextmanager
    def world_canvas(self):
        renderer = Renderer.get_current()
        with renderer.canvas_target() as canvas:
            canvas.save()
            canvas.translate(
                renderer.viewport.width // 2, renderer.viewport.height // 2
            )
            scale = self._camera_scale()
            canvas.scale(scale, -scale)  # world units -> px, invert Y for Skia
            camera = renderer.camera_2d
            canvas.translate(-camera.position.x, -camera.position.y)
            try:
                yield canvas
            finally:
                canvas.restore()

    def _scaled_stroke_width(self) -> float:
        renderer = Renderer.get_current()
        # scale = renderer.camera_2d.ppu / renderer.camera_2d.zoom
        scale = self.ppu / renderer.camera_2d.zoom
        return self.outline_width_px / scale

    def _draw(self):
        with self.world_canvas() as canvas:
            self.draw_items()

    """
    def _draw(self):
        renderer = Renderer.get_current()
        with renderer.canvas_target() as canvas:
            canvas.save()

            canvas.translate(
                renderer.viewport.width // 2, renderer.viewport.height // 2
            )
            scale = renderer.camera_2d.ppu / renderer.camera_2d.zoom
            canvas.scale(scale, -scale)  # world units -> pixels, invert Y for Skia
            camera_x, camera_y = (
                renderer.camera_2d.position.x,
                renderer.camera_2d.position.y,
            )
            canvas.translate(-camera_x, -camera_y)  # pan to camera

            self.draw_items()

            canvas.restore()

        super()._draw()
    """

    def draw_items(self):
        pass  # Implement in subclasses to draw specific items in world space
