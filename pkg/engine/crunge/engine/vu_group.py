from typing import Any, TypeVar, Generic, List

from loguru import logger

from .vu import Vu
from .chip import Chip

T_Vu = TypeVar("T_Vu", bound=Vu)


class VuGroup(Chip[Any], Generic[T_Vu]):
    """A batch of vus drawn together.

    A chip rather than a free-standing object: it has an update and a draw
    and a lifetime, which is what a chip is. Mounted on the node that owns
    the batch — for a graph layer, that is the layer's root — so the chip
    walk drives it and no container has to remember to forward.
    """

    def __init__(self):
        super().__init__()
        self.visuals: List[T_Vu] = []
        self.is_render_group = False

    def append(self, vu: T_Vu) -> None:
        if vu in self.visuals:
            raise ValueError("Vu already in group")
        self.visuals.append(vu)
        # Last: on_group fires from the setter, and a subclass appending
        # buffer state does it after this returns. The vu marks dirt and
        # the write lands on the next flush.
        vu.group = self

    def extend(self, members: List[T_Vu]) -> None:
        # Was a bare list extend, which skipped the group assignment
        # entirely — vus added this way never got on_group.
        for vu in members:
            self.append(vu)

    def remove(self, vu: T_Vu) -> None:
        logger.debug(f"Removing {vu} from {self}")
        self.visuals.remove(vu)
        vu.group = None

    def clear(self) -> None:
        for vu in tuple(self.visuals):
            vu.group = None
        self.visuals.clear()

    def __len__(self) -> int:
        return len(self.visuals)

    def __iter__(self):
        return iter(self.visuals)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        for vu in self.visuals:
            vu.draw()

    def update(self, delta_time: float) -> None:
        for vu in self.visuals:
            vu.update(delta_time)