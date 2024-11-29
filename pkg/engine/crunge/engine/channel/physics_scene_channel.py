from ..factory import Factory
from ..view import View
from ..scene import Scene
from ..physics_engine import PhysicsEngine

from .scene_channel import SceneChannel


class PhysicsSceneChannel(SceneChannel):
    def __init__(
        self,
        view_factory: Factory[View],
        scene_factory: Factory[Scene],
        physics_engine_factory: Factory[PhysicsEngine],
        name: str,
        title: str = None,
    ) -> None:
        super().__init__(view_factory, scene_factory, name, title)
        self.physics_engine_factory = physics_engine_factory

    def produce_physics_engine(self, *args, **kwargs) -> PhysicsEngine:
        return self.physics_engine_factory(*args, **kwargs)

    def produce_scene(self, *args, **kwargs) -> Scene:
        physics_engine = self.produce_physics_engine()
        return self.scene_factory(self.name, physics_engine, *args, **kwargs)

    def produce_view(self, *args, **kwargs) -> View:
        scene = self.produce_scene()
        view = super().produce_view(scene)
        return view
