from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from .. import engine
from ..wyggle import Wyggle

WYGGLE_COUNT = 3
# WYGGLE_COUNT = 1


class WyggleLayer(GraphLayer2D):
    def __init__(self, name: str = "wyggle") -> None:
        super().__init__(name)
        self.wyggles: list[Wyggle] = []

    def create_children(self):
        super().create_children()
        for _ in range(WYGGLE_COUNT):
            self.spawn_wyggle()

    def spawn_wyggle(self):
        wyggle = Wyggle()
        engine.sprite_engine.materialize_random_from_center(wyggle, self)

    def add_wyggle(self, wyggle: Wyggle) -> None:
        self.wyggles.append(wyggle)
        self.add_node(wyggle.node)

    def remove_wyggle(self, wyggle: Wyggle) -> None:
        if wyggle in self.wyggles:
            self.wyggles.remove(wyggle)
            self.remove_node(wyggle.node)
