from ...renderer import Renderer
from ...base import Base

from . import Sprite

class SpriteGroup(Base):
    def __init__(self):
        self.sprites: list[Sprite] = []
        self.is_render_group = False

    def append(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)

    def extend(self, sprites: list[Sprite]) -> None:
        self.sprites.extend(sprites)

    def remove(self, sprite: Sprite) -> None:
        self.sprites.remove(sprite)

    def clear(self) -> None:
        self.sprites.clear()

    def __len__(self) -> int:
        return len(self.sprites)

    def __iter__(self):
        return iter(self.sprites)

    def __repr__(self) -> str:
        return f"<SpriteList: {len(self)} sprites>"

    def __str__(self) -> str:
        return repr(self)
    
    def draw(self, renderer: Renderer) -> None:
        for sprite in self.sprites:
            projection = renderer.camera_2d.projection
            if sprite.aabb.intersects(projection):
                sprite.draw(renderer)

    def update(self, delta_time: float) -> None:
        for sprite in self.sprites:
            sprite.update(delta_time)