from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from ...base import Base

if TYPE_CHECKING:
    from .. import Renderer

T_Renderer = TypeVar("T_Renderer", bound="Renderer")


class RenderPhase(Generic[T_Renderer], Base):
    def __init__(self, renderer: T_Renderer) -> None:
        super().__init__()
        self.renderer = renderer

    def clear(self) -> None:
        pass

    def render(self) -> None:
        pass
