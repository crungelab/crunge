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
        self.members: List[T_Vu] = []
        self.is_render_group = False

    def append(self, member: T_Vu) -> None:
        if member in self.members:
            raise ValueError(f"{member} already in group")
        self.members.append(member)
        # Last: on_group fires from the setter, and a subclass appending
        # buffer state does it after this returns. The vu marks dirt and
        # the write lands on the next flush.
        member.group = self

    def extend(self, members: List[T_Vu]) -> None:
        # Was a bare list extend, which skipped the group assignment
        # entirely — vus added this way never got on_group.
        for member in members:
            self.append(member)

    def remove(self, member: T_Vu) -> None:
        logger.debug(f"Removing {member} from {self}")
        self.members.remove(member)
        member.group = None

    def clear(self) -> None:
        for member in tuple(self.members):
            member.group = None
        self.members.clear()

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        for member in self.members:
            member.draw()

    def update(self, delta_time: float) -> None:
        for member in self.members:
            member.update(delta_time)