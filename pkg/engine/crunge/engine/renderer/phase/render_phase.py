from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from ...base import Base

if TYPE_CHECKING:
    from .. import Renderer

T = TypeVar("T", bound="Renderer")

class RenderPhase(Generic[T], Base):
    def __init__(self, renderer: T) -> None:
        super().__init__()
        self.renderer = renderer

    def render(self) -> None:
        pass
