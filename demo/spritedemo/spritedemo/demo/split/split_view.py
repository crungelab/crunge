from loguru import logger

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.viewport import Viewport
from crunge.engine.math import Rect2i


class SplitView(SceneView2D):
    def create_camera(self):
        self.camera = Camera2D()

    def create_renderer(self) -> None:
        self.renderer = Renderer2D(self.viewport, camera=self.camera, clear=False)

    def create_viewport(self):
        parent = Viewport.get_current()
        self.viewport = parent.add_child(Viewport())

    def on_layout(self) -> None:
        super().on_layout()
        if self.viewport is not None:
            pos, size = self.global_position, self.size
            self.viewport.rect = Rect2i(pos.x, pos.y, size.x, size.y)

"""
class SplitView(SceneView2D):
    def create_camera(self):
        self.camera = Camera2D()

    def create_viewport(self):
        current_viewport = Viewport.get_current()
        current_easel = current_viewport.easel if current_viewport else None
        logger.debug(f"Creating viewport for SplitView, current_easel: {current_easel}, width: {self.width}, height: {self.height}")
        self.viewport = Viewport(
            current_easel,
            Rect2i(0, 0, self.width, self.height),
        )
        logger.debug(f"Created viewport: {self.viewport}, width: {self.width}, height: {self.height}")

    def on_layout(self) -> None:
        super().on_layout()
        if self.viewport is not None:
            pos, size = self.global_position, self.size
            self.viewport.rect = Rect2i(pos.x, pos.y, size.x, size.y)
"""