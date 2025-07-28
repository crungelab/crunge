from typing import TypeVar, Generic, List

from ...base import Base
from .model import Model

T_Model = TypeVar("T_Model", bound=Model)


class ModelGroup(Base, Generic[T_Model]):
    def __init__(self):
        super().__init__()
        self.models: List[T_Model] = []

    def append(self, model: T_Model) -> None:
        self.models.append(model)

    def extend(self, members: List[T_Model]) -> None:
        self.models.extend(members)

    def remove(self, model: T_Model) -> None:
        self.models.remove(model)

    def clear(self) -> None:
        self.models.clear()

    def __len__(self) -> int:
        return len(self.models)

    def __iter__(self):
        return iter(self.models)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)
