from loguru import logger

from crunge.engine.d2.screen import SceneScreen2D

from .demo_view import DemoView

class DemoScreen(SceneScreen2D):
    def create_children(self):
        logger.debug("Creating screen children")
        self.view = DemoView(self.scene).enable()
        self.add_child(self.view)
