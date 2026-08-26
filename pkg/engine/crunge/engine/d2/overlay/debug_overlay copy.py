from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass

from loguru import logger

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
        current_renderer = Renderer.get_current()
        camera = current_renderer.camera_2d
        #logger.debug(f"Renderer: {current_renderer}")
        return camera.ppu / camera.zoom

    @contextmanager
    def world_canvas(self):
        renderer = Renderer.get_current()
        rect = renderer.viewport.global_rect
        with renderer.canvas_target() as canvas:
            canvas.save()
            canvas.translate(
                rect.x + rect.width // 2,
                rect.y + rect.height // 2,
            )
            scale = self._camera_scale()
            canvas.scale(scale, -scale)
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

    def draw_items(self):
        pass  # Implement in subclasses to draw specific items in world space
