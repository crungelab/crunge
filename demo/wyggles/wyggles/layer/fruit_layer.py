from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from .. import world
from ..fruit import Fruit, FruitFactory

FOOD_COUNT = 3
# FOOD_COUNT = 10

class FruitLayer(GraphLayer2D):
    def __init__(self, name: str = "fruit") -> None:
        super().__init__(name)
        self.fruits: list[Fruit] = []
        self.respawning_food = False

    def create_children(self):
        super().create_children()
        for _ in range(FOOD_COUNT):
            self.spawn_fruit()

    def spawn_fruit(self):
        fruitFactory = FruitFactory(self)
        fruit = fruitFactory.create_random()
        world.world_instance.materialize_random_from_center(fruit, self)

    def add_fruit(self, fruit: Fruit) -> None:
        self.fruits.append(fruit)
        self.add_node(fruit.node)

    def remove_fruit(self, fruit: Fruit) -> None:
        if fruit in self.fruits:
            self.fruits.remove(fruit)
            self.remove_node(fruit.node)

    def update(self, delta_time: float):
        if len(self) < FOOD_COUNT and not self.respawning_food:
            self.respawning_food = True

            def re_spawn(delta_time: float):
                self.spawn_fruit()
                self.respawning_food = False

            Scheduler().schedule_once(re_spawn, 3.0)

        super().update(delta_time)
