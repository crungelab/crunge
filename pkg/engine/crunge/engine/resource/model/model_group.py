from typing import TypeVar, Generic, List

from ...base import Base
from .model import ModelMembership

T_Membership = TypeVar("T_Membership", bound=ModelMembership)


class ModelGroup(Base, Generic[T_Membership]):
    def __init__(self):
        super().__init__()
        self.memberships: List[T_Membership] = []

    def append(self, model: T_Membership) -> None:
        self.memberships.append(model)

    def extend(self, members: List[T_Membership]) -> None:
        self.memberships.extend(members)

    def remove(self, model: T_Membership) -> None:
        self.memberships.remove(model)

    def clear(self) -> None:
        self.memberships.clear()

    def __len__(self) -> int:
        return len(self.memberships)

    def __iter__(self):
        return iter(self.memberships)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)
