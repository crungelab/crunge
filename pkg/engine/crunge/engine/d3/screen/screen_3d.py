from loguru import logger

from ...screen import Screen

from ..view import View3D

from ..camera_3d import Camera3D

class Screen3D(Screen):
    def __init__(self, name: str = "Screen3D", title: str = "Screen 3D") -> None:
        super().__init__(name=name, title=title)

    @property
    def primary_camera_3d(self) -> Camera3D:
        return self.primary_view.primary_camera_3d

    def create_views(self):
        logger.debug("Creating screen views")
        self.view = View3D()
        self.add_child(self.view)
