from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ....vu import Vu
    from ....model import Model


from ..scene_layer import SceneLayer

class FilterLayer(SceneLayer):
    def __init__(self, name: str, vu: "Vu" = None, model: "Model" = None) -> None:
        super().__init__(name=name, vu=vu, model=model)
