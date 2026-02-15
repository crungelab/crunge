from loguru import logger

from .render_task import RenderTask


class RenderPhase(RenderTask):
    def __init__(self) -> None:
        super().__init__()