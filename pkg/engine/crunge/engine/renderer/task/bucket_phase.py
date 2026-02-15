from typing import Generic, TypeVar

from loguru import logger

from .render_phase import RenderPhase

T_PhaseItem = TypeVar("T_PhaseItem")


class BucketPhase(Generic[T_PhaseItem], RenderPhase):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[T_PhaseItem] = []

    def clear(self) -> None:
        self.items.clear()

    def add(self, item: T_PhaseItem) -> None:
        self.items.append(item)

    def sort(self) -> None:
        # Optional; override in subclasses
        pass
