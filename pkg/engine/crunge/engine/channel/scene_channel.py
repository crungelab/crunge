from ..factory import Factory
from ..view import View
from ..scene import Scene

from .channel import Channel


class SceneChannel(Channel):
    def __init__(self, view_factory: Factory[View], scene_factory: Factory[Scene], name: str, title: str = None) -> None:
        super().__init__(view_factory, name, title)
        self.scene_factory = scene_factory
    
    def produce_scene(self, *args, **kwargs) -> View:
        #return self.scene_factory(*args, **kwargs)
        return self.scene_factory(self.name, *args, **kwargs)
    
    def produce_view(self, *args, **kwargs) -> View:
        scene = self.produce_scene()
        view = super().produce_view(scene)
        return view