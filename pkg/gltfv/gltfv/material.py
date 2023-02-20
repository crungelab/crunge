from .texture import Texture

class Material:
    textures: list[Texture] = None
    base_color_texture: Texture = None
    emissive_factor: tuple = (0, 0, 0)
    emissive_texture: Texture = None

    def __init__(self) -> None:
        self.textures = []

    def add_texture(self, texture: Texture):
        self.textures.append(texture)
