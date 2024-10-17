from crunge import wgpu

from .resource import Resource
from .texture import Texture


class Material(Resource):
    textures: list[Texture] = None
    texture_set: set = None

    def __init__(self) -> None:
        super().__init__()
        self.textures = []
        self.texture_set = set()

    def add_texture(self, texture: Texture):
        self.textures.append(texture)
        self.texture_set.add(texture.name)

    def has_texture(self, name: str) -> bool:
        return name in self.texture_set

    @property
    def has_base_color_texture(self):
        return self.has_texture('baseColor')
    
    @property
    def has_metallic_roughness_texture(self):
        return self.has_texture('metallicRoughness')
    
    @property
    def has_normal_texture(self):
        return self.has_texture('normal')

    @property
    def has_occlusion_texture(self):
        return self.has_texture('occlusion')
    
    @property
    def has_emissive_texture(self):
        return self.has_texture('emissive')

    @property
    def has_environment_texture(self):
        return self.has_texture('environment')
