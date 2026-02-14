from typing import TYPE_CHECKING, Optional
import contextlib
from contextvars import ContextVar

import glm
from crunge import tmx

from crunge.engine.scene.layer.scene_layer import SceneLayer
from crunge.engine.scene.layer.layer_group import LayerGroup
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.graph_layer_2d import GraphLayer2D
from crunge.engine.d2.sprite import Sprite

if TYPE_CHECKING:
    from .map_builder import MapBuilder

builder_context: ContextVar[Optional["BuilderContext"]] = ContextVar("builder_context", default=None)

class BuilderContext:
    def __init__(self, scene: Scene2D):
        self.scene = scene
        self.layer_stack: list[SceneLayer] = []
        #self.layer: GraphLayer2D = None
        self.map_builder: "MapBuilder" = None

        self._map: tmx.Map = None
        self.size = glm.ivec2()
        self.opacity: float = 1.0

        self.sprites: list[Sprite] = []

        self.push_layer(scene)

    def make_current(self):
        builder_context.set(self)

    @classmethod
    def get_current(cls) -> Optional["BuilderContext"]:
        return builder_context.get()

    @property
    def current_layer(self) -> Optional[SceneLayer]:
        if self.layer_stack:
            return self.layer_stack[-1]
        return None

    @property
    def current_layer_group(self) -> Optional[LayerGroup]:
        layer = self.current_layer
        if isinstance(layer, LayerGroup):
            return layer
        raise TypeError("Current layer is not a LayerGroup")

    @property
    def current_graph_layer(self) -> Optional[GraphLayer2D]:
        layer = self.current_layer
        if isinstance(layer, GraphLayer2D):
            return layer
        raise TypeError("Current layer is not a GraphLayer2D")

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map: tmx.Map):
        self._map = map
        tile_size = map.tile_size
        tw = tile_size.x
        th = tile_size.y

        tile_count = map.tile_count
        mw = tile_count.x
        mh = tile_count.y - 1
        self.size = glm.ivec2(mw * tw, mh * th)

    def init_sprites(self, count: int):
        self.sprites = [None] * count

    def push_layer(self, layer: SceneLayer):
        self.layer_stack.append(layer)

    def pop_layer(self) -> SceneLayer:
        return self.layer_stack.pop()