from .texture import Texture

class Material:
    textures: list[Texture] = None
    texture_set: set = None

    alpha_mode: str = 'BLEND'
    # (3,) or (4,) float with RGBA colors
    base_color_factor = (0, 0, 0, 0)
    #base_color_texture: Texture = None

    metallic_factor: float = 0
    roughness_factor: float = 0
    #metallic_roughness_texture: Texture = None

    #normal_texure: Texture = None
    #occlusion_texure: Texture = None
    # (3,) float
    emissive_factor: tuple = (0, 0, 0)
    #emissive_texture: Texture = None

    def __init__(self) -> None:
        self.textures = []
        self.texture_set = set()

    def add_texture(self, texture: Texture):
        self.textures.append(texture)
        self.texture_set.add(texture.name)

    def has_texture(self, name: str) -> bool:
        return name in self.texture_set
