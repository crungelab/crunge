from ..factory import Factory
from ..display import Display
from ..scene import Scene
from ..physics_engine import PhysicsEngine

from .scene_channel import SceneChannel


class PhysicsSceneChannel(SceneChannel):
    def __init__(
        self,
        display_factory: Factory[Display],
        scene_factory: Factory[Scene],
        physics_engine_factory: Factory[PhysicsEngine],
        name: str,
        title: str = None,
        next_channel: str = None,
    ) -> None:
        super().__init__(display_factory, scene_factory, name, title, next_channel)
        self.physics_engine_factory = physics_engine_factory

    def produce_physics_engine(self, *args, **kwargs) -> PhysicsEngine:
        return self.physics_engine_factory(*args, **kwargs)

    def produce_scene(self, *args, **kwargs) -> Scene:
        physics_engine = self.produce_physics_engine()
        return self.scene_factory(self.name, physics_engine, *args, **kwargs)
