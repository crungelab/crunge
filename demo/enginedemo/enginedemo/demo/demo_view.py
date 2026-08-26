from loguru import logger

from crunge.engine.view import View


class DemoView(View):
    def __init__(self, overlays=[]):
        super().__init__(overlays=overlays)
