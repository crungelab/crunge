from typing import TypeVar, Generic, List

from ...base import Base
from .material import Material

T_Material = TypeVar("T_Material", bound=Material)


class MaterialGroup(Base, Generic[T_Material]):
    def __init__(self):
        super().__init__()
        self.materials: List[T_Material] = []

    def append(self, vu: T_Material) -> None:
        self.materials.append(vu)

    def extend(self, members: List[T_Material]) -> None:
        self.materials.extend(members)

    def remove(self, vu: T_Material) -> None:
        self.materials.remove(vu)

    def clear(self) -> None:
        self.materials.clear()

    def __len__(self) -> int:
        return len(self.materials)

    def __iter__(self):
        return iter(self.materials)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: length={len(self)}>"

    def __str__(self) -> str:
        return repr(self)
