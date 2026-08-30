from typing import Generic, Iterator, List, TypeVar

from loguru import logger

from .chip import Chip

class Grouped:
    """Protocol-ish base for anything that can belong to a Group."""

    _group: "Group | None" = None

    @property
    def group(self) -> "Group | None":
        return self._group

    @group.setter
    def group(self, value: "Group | None") -> None:
        self._group = value
        self.on_group()

    def on_group(self) -> None:
        pass


T = TypeVar("T", bound=Grouped)


class Group(Generic[T]):
    """Membership list that keeps each member's back-reference in sync."""

    def __init__(self):
        super().__init__()
        self.members: List[T] = []

    def append(self, member: T) -> None:
        if member in self.members:
            raise ValueError(f"{member} already in group")
        self.members.append(member)
        # Last: on_group fires from the setter, and a subclass appending
        # buffer state does it after this returns.
        member.group = self

    def extend(self, members: List[T]) -> None:
        for member in members:
            self.append(member)

    def remove(self, member: T) -> None:
        logger.debug(f"Removing {member} from {self}")
        self.members.remove(member)
        member.group = None

    def clear(self) -> None:
        for member in tuple(self.members):
            member.group = None
        self.members.clear()

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self) -> Iterator[T]:
        return iter(self.members)

    def __contains__(self, member: T) -> bool:
        return member in self.members

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)