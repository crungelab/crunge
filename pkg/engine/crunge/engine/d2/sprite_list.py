from ..renderer import Renderer
from .sprite import Sprite

class SpriteList:
    def __init__(self):
        self.sprites: list[Sprite] = []

    def append(self, sprite):
        self.sprites.append(sprite)

    def clear(self):
        self.sprites.clear()

    def __len__(self):
        return len(self.sprites)

    def __iter__(self):
        return iter(self.sprites)

    def __repr__(self):
        return f"<SpriteList: {len(self)} sprites>"

    def __str__(self):
        return repr(self)
    
    def draw(self, renderer: Renderer):
        for sprite in self.sprites:
            sprite.draw(renderer)

    def update(self, delta_time: float):
        for sprite in self.sprites:
            sprite.update(delta_time)