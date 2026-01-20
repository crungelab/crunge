from typing import Generic, TypeVar

from loguru import logger

from .render_phase import RenderPhase, T_Renderer

T_PhaseItem = TypeVar("T_PhaseItem")


class ItemPhase(Generic[T_Renderer, T_PhaseItem], RenderPhase[T_Renderer]):
    def __init__(self, renderer: T_Renderer) -> None:
        super().__init__(renderer)
        self.items: list[T_PhaseItem] = []

    def clear(self) -> None:
        self.items.clear()

    def add(self, item: T_PhaseItem) -> None:
        self.items.append(item)

    def sort(self) -> None:
        # Optional; override in subclasses
        pass
