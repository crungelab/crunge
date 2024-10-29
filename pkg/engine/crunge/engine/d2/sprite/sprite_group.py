from ...renderer import Renderer
from . import Sprite

class SpriteGroup:
    def __init__(self):
        self.sprites: list[Sprite] = []
        self.is_render_group = False

    def append(self, sprite):
        self.sprites.append(sprite)

    def extend(self, sprites):
        self.sprites.extend(sprites)

    def remove(self, sprite):
        self.sprites.remove(sprite)

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
            projection = renderer.camera.projection
            if sprite.aabb.intersects(projection):
                sprite.draw(renderer)

    def update(self, delta_time: float):
        for sprite in self.sprites:
            sprite.update(delta_time)