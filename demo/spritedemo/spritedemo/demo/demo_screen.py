from loguru import logger

from crunge.engine.d2.screen import SceneScreen2D

from .demo_view import DemoView

class DemoScreen(SceneScreen2D):
    @property
    def camera(self):
        return self.view.camera

    @property
    def renderer(self):
        return self.view.renderer
    
    def create_views(self):
        logger.debug("Creating screen views")
        self.view = DemoView(self.scene)
        self.add_child(self.view)
