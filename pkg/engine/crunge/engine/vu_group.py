from typing import TypeVar, Generic, List

from .renderer import Renderer
from .vu import Vu

T_Vu = TypeVar("T_Vu", bound=Vu)


class VuGroup(Vu, Generic[T_Vu]):
    def __init__(self):
        super().__init__()
        self.visuals: List[T_Vu] = []
        self.is_render_group = False

    def append(self, vu: T_Vu) -> None:
        vu.group = self
        self.visuals.append(vu)

    def extend(self, members: List[T_Vu]) -> None:
        self.visuals.extend(members)

    def remove(self, vu: T_Vu) -> None:
        '''
        if not vu in self.visuals:
            return
        '''
        self.visuals.remove(vu)

    def clear(self) -> None:
        self.visuals.clear()

    def __len__(self) -> int:
        return len(self.visuals)

    def __iter__(self):
        return iter(self.visuals)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)

    def draw(self, renderer: Renderer) -> None:
        for vu in self.visuals:
            vu.draw(renderer)

    def update(self, delta_time: float) -> None:
        for vu in self.visuals:
            vu.update(delta_time)
