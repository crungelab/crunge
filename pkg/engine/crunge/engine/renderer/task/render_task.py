from loguru import logger

from ...base import Base

from ..renderer import Renderer


class RenderTask(Base):
    def __init__(self) -> None:
        super().__init__()

    @property
    def renderer(self) -> Renderer:
        return Renderer.get_current()

    def clear(self) -> None:
        pass

    def render(self) -> None:
        pass
