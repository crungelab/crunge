from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from ...base import Base

if TYPE_CHECKING:
    from .. import Renderer

#T_Renderer = TypeVar("T_Renderer", bound="Renderer")
from .render_task import RenderTask, T_Renderer


class RenderPhase(RenderTask[T_Renderer]):
    def __init__(self, renderer: T_Renderer) -> None:
        super().__init__(renderer)
