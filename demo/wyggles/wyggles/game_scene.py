import timeit

from loguru import logger
from crunge.engine.d2.scene.physics_scene_2d import PhysicsScene2D
from crunge.engine.d2.entity import StaticEntity2D

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultObjectBuilder

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder.builder_context import BuilderContext
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

import wyggles.globe
from .world import World

from .layer import WallLayer, FruitLayer, BallLayer, WyggleLayer


class StaticObjectGroupBuilder(tiled_builder.DefaultObjectGroupBuilder):
    def __init__(self):
        def create_node_cb(position, rotation, scale, sprite, properties: dict):
            logger.debug(f"create_node_cb: {position}, {sprite}, {properties}")
            node = StaticEntity2D(position, rotation, scale, model=sprite)
            return node

        super().__init__(
            object_builder=DefaultObjectBuilder(create_node_cb=create_node_cb),
        )


class GameScene(PhysicsScene2D):
    def __init__(self, name: str):
        super().__init__(World())
        self.name = name
        self.paused = False

    def _create(self):
        self.create_map()

        wyggles.globe.landscape_layer = self.landscape_layer = self.get_layer(
            "landscape"
        )

        self.wall_layer = WallLayer("walls")
        self.add_layer(self.wall_layer)

        self.fruit_layer = FruitLayer("fruit")
        self.add_layer(self.fruit_layer)

        self.ball_layer = BallLayer("balls")
        self.add_layer(self.ball_layer)

        self.wyggle_layer = WyggleLayer("wyggles")
        self.add_layer(self.wyggle_layer)

    def create_map(self):
        tmx_path = ResourceManager().resolve_path("${resources}/level1.tmx")
        context = BuilderContext(scene=self)
        map_builder = DefaultMapBuilder()
        map_builder.add_object_group_builder("landscape", StaticObjectGroupBuilder())
        map_loader = TiledMapLoader(context, map_builder=map_builder)
        map_loader.load(tmx_path)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def update(self, delta_time: float):
        start_time = timeit.default_timer()

        self.world.update(1 / 60.0)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

        super().update(delta_time)
