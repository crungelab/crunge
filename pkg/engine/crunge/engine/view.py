from typing import TYPE_CHECKING

from loguru import logger

from .widget import Display, Overlay


class View(Display):
    def __init__(self, overlays: list[Overlay] = None) -> None:
        super().__init__(overlays)

    def _create(self):
        # logger.debug("View.create")
        super()._create()
        self.create_device_objects()
        self.create_camera()
        self.create_renderer()

    def create_device_objects(self):
        pass

    def create_camera(self):
        pass

    def create_renderer(self):
        pass
