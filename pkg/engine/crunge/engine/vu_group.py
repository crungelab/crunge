from typing import TypeVar, Generic, List

from .renderer import Renderer
from .vu import Vu

T_Vu = TypeVar("T_Vu")


class VuGroup(Vu, Generic[T_Vu]):
    def __init__(self):
        self.members: List[T_Vu] = []
        self.is_render_group = False

    def append(self, vu: T_Vu) -> None:
        self.members.append(vu)

    def extend(self, members: List[T_Vu]) -> None:
        self.members.extend(members)

    def remove(self, vu: T_Vu) -> None:
        self.members.remove(vu)

    def clear(self) -> None:
        self.members.clear()

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)

    def draw(self, renderer: Renderer) -> None:
        for vu in self.members:
            vu.draw(renderer)

    def update(self, delta_time: float) -> None:
        for vu in self.members:
            vu.update(delta_time)
