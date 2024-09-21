from ..resource.texture import Texture

from .sprite_animation import SpriteAnimation


class FrameAnimation(SpriteAnimation):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.frames: list[Texture] = []
