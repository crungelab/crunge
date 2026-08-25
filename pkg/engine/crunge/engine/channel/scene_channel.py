from ..factory import Factory
from ..display import Display
from ..scene import Scene

from .channel import Channel


class SceneChannel(Channel):
    def __init__(
        self,
        display_factory: Factory[Display],
        scene_factory: Factory[Scene],
        name: str,
        title: str = None,
        next_channel: str = None,
    ) -> None:
        super().__init__(display_factory, name, title, next_channel)
        self.scene_factory = scene_factory

    def produce_scene(self, *args, **kwargs) -> Scene:
        return self.scene_factory(self.name, *args, **kwargs)

    def produce_display(self, *args, **kwargs) -> Display:
        scene = self.produce_scene()
        return super().produce_display(scene, *args, **kwargs)
