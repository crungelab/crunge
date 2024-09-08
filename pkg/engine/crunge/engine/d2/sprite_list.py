from ..renderer import Renderer
from .sprite import Sprite

class SpriteList:
    def __init__(self):
        self.sprites: list[Sprite] = []
        self.sprites_by_id = {}
        self.sprites_by_name = {}

    def add(self, sprite):
        self.sprites.append(sprite)
        self.sprites_by_id[sprite.id] = sprite
        self.sprites_by_name[sprite.name] = sprite

    def get_by_id(self, id):
        return self.sprites_by_id.get(id)

    def get_by_name(self, name):
        return self.sprites_by_name.get(name)

    def get_by_index(self, index):
        return self.sprites[index]

    def __len__(self):
        return len(self.sprites)

    def __iter__(self):
        return iter(self.sprites)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.get_by_index(key)
        elif isinstance(key, str):
            return self.get_by_name(key)
        else:
            raise TypeError("key must be int or str")

    def __contains__(self, key):
        if isinstance(key, int):
            return key < len(self)
        elif isinstance(key, str):
            return key in self.sprites_by_name
        else:
            raise TypeError("key must be int or str")

    def __repr__(self):
        return f"<SpriteList: {len(self)} sprites>"

    def __str__(self):
        return repr(self)
    
    def draw(self, renderer: Renderer):
        for sprite in self.sprites:
            sprite.draw(renderer)