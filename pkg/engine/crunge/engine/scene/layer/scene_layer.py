from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from ... import Base

if TYPE_CHECKING:
    from .. import Scene


class SceneLayer(Base):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.scene: Scene = None

    def clear(self) -> None:
        pass
    
    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass