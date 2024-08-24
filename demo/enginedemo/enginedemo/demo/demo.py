from pathlib import Path

from loguru import logger
import glm

from crunge import engine

from .demo_view import DemoView

class Demo(engine.App):
    kWidth = 1024
    kHeight = 768

    def __init__(self, view=DemoView()):
        super().__init__(
            glm.ivec2(self.kWidth, self.kHeight),
            self.__class__.__name__,
            view=view,
            resizable=True,
        )
        self.resource_root = Path(__file__).parent.parent.parent.parent.parent / "resources"
