from loguru import logger
from .demo import Demo

from .scrolling_demo_controller import ScrollingDemoController

class ScrollingDemo(Demo):
    def setup(self):
        super().setup()
        #self.controller = ScrollingDemoController(self.camera)