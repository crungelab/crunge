from .texture import Texture

class Material:
    # (3,) or (4,) float with RGBA colors
    base_color_factor = (0, 0, 0, 0)
    textures: list[Texture] = None
    base_color_texture: Texture = None

    metallic_factor: float = 0
    roughness_factor: float = 0
    metallic_roughness_texure: Texture = None

    normal_texure: Texture = None

    # (3,) float
    emissive_factor: tuple = (0, 0, 0)
    emissive_texture: Texture = None

    def __init__(self) -> None:
        self.textures = []

    def add_texture(self, texture: Texture):
        self.textures.append(texture)
