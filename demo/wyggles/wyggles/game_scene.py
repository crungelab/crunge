import timeit

from loguru import logger
import glm

from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer import GraphLayer2D
from crunge.engine.d2.scene.physics_scene_2d import PhysicsScene2D
from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.physics import BoxGeom
from crunge.engine.d2.sprite import SpriteVu

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultObjectBuilder

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder.builder_context import BuilderContext
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

from . import engine
from .engine import world_left, world_right, world_top, world_bottom

import wyggles.globe
from .engine import SpriteEngine
from .wyggle import Wyggle
from .ball import Ball
from .fruit import FruitFactory

WYGGLE_COUNT = 3
# WYGGLE_COUNT = 1

FOOD_COUNT = 3
# FOOD_COUNT = 10

BALL_COUNT = 10


def spawn_wyggle(layer):
    wyggle = Wyggle()
    engine.sprite_engine.materialize_random_from_center(wyggle, layer)


def spawn_wyggles(layer):
    for _ in range(WYGGLE_COUNT):
        spawn_wyggle(layer)


# Balls
def spawn_ball(layer):
    ball = Ball()
    engine.sprite_engine.materialize_random_from_center(ball, layer)


def spawn_balls(layer):
    for _ in range(BALL_COUNT):
        spawn_ball(layer)


def spawn_food(layer):
    fruitFactory = FruitFactory(layer)
    for _ in range(FOOD_COUNT):
        fruit = fruitFactory.create_random()
        engine.sprite_engine.materialize_random_from_center(fruit, layer)


def spawn_fruit(layer):
    fruitFactory = FruitFactory(layer)
    fruit = fruitFactory.create_random()
    engine.sprite_engine.materialize_random_from_center(fruit, layer)


class Barrier(StaticEntity2D):
    def __init__(self, left: float, bottom: float, right: float, top: float):
        width = right - left
        height = top - bottom
        position = glm.vec2(left + width / 2, bottom + height / 2)
        super().__init__(position, scale=glm.vec2(width, height), geom=BoxGeom())


# Walls
def spawn_wall(layer, left: float, bottom: float, right: float, top: float):
    node = Barrier(left, bottom, right, top)
    layer.attach(node)


def spawn_walls(layer):
    left = world_left
    bottom = world_bottom
    right = world_right
    top = world_top
    thickness = 200
    # North Wall
    spawn_wall(layer, left - thickness, top, right + thickness, top + thickness)
    # South Wall
    spawn_wall(layer, left - thickness, bottom - thickness, right + thickness, bottom)
    # East Wall
    spawn_wall(layer, right, bottom - thickness, right + thickness, top + thickness)
    # West Wall
    spawn_wall(layer, left - thickness, bottom - thickness, left, top + thickness)


class StaticObjectGroupBuilder(tiled_builder.DefaultObjectGroupBuilder):
    def __init__(self):
        def create_node_cb(position, rotation, scale, sprite, properties: dict):
            logger.debug(f"create_node_cb: {position}, {sprite}, {properties}")
            node = StaticEntity2D(
                position, rotation, scale, model=sprite
            )
            return node

        super().__init__(
            object_builder=DefaultObjectBuilder(create_node_cb=create_node_cb),
        )


class GameScene(PhysicsScene2D):
    def __init__(self, name: str):
        super().__init__(SpriteEngine())
        self.name = name
        self.paused = False
        self.respawning_food = False

    def _create(self):
        self.create_map()

        wyggles.globe.landscape_layer = self.landscape_layer = self.get_layer(
            "landscape"
        )

        self.wyggle_layer = GraphLayer2D("wyggles")
        self.add_layer(self.wyggle_layer)
        spawn_wyggles(self.wyggle_layer)

        self.ball_layer = GraphLayer2D("balls")
        self.add_layer(self.ball_layer)
        spawn_balls(self.ball_layer)

        self.food_layer = GraphLayer2D("food")
        self.add_layer(self.food_layer)
        spawn_food(self.food_layer)

        # Lists of sprites or lines
        self.wall_layer = GraphLayer2D("walls")
        self.add_layer(self.wall_layer)
        spawn_walls(self.wall_layer)

    def create_map(self):
        tmx_path = ResourceManager().resolve_path("${resources}/level1.tmx")
        context = BuilderContext(scene=self)
        map_builder = DefaultMapBuilder()
        map_builder.add_object_group_builder(
            "landscape", StaticObjectGroupBuilder()
        )
        map_loader = TiledMapLoader(context, map_builder=map_builder)
        map_loader.load(tmx_path)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def update(self, delta_time: float):
        start_time = timeit.default_timer()

        if len(self.food_layer) < FOOD_COUNT and not self.respawning_food:
            self.respawning_food = True

            def re_spawn(delta_time: float):
                spawn_fruit(self.food_layer)
                self.respawning_food = False

            Scheduler().schedule_once(re_spawn, 3.0)

        #self.space.step(1 / 60.0)
        #self.world.update(delta_time)
        self.world.update(1 / 60.0)


        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

        super().update(delta_time)
