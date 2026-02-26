from loguru import logger
from .demo import Demo

from .scrolling_demo_controller import ScrollingDemoController

class ScrollingDemo(Demo):
    def reset(self):
        super().reset()
        self.controller = ScrollingDemoController(self.camera)