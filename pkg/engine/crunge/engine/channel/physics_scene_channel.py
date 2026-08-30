from ..factory import Factory
from ..display import Display
from ..scene import Scene
from ..world import PhysicsEngine

from .scene_channel import SceneChannel


class PhysicsSceneChannel(SceneChannel):
    def __init__(
        self,
        display_factory: Factory[Display],
        scene_factory: Factory[Scene],
        world_factory: Factory[PhysicsEngine],
        name: str,
        title: str = None,
        next_channel: str = None,
    ) -> None:
        super().__init__(display_factory, scene_factory, name, title, next_channel)
        self.world_factory = world_factory

    def produce_world(self, *args, **kwargs) -> PhysicsEngine:
        return self.world_factory(*args, **kwargs)

    def produce_scene(self, *args, **kwargs) -> Scene:
        world = self.produce_world()
        return self.scene_factory(self.name, world, *args, **kwargs)
