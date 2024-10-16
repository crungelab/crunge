from crunge import wgpu

from ..resource.material import Material
from ..resource.texture import Texture
#from .bind_group_layout import BindGroupLayout


class Material3D(Material):
    textures: list[Texture] = None
    texture_set: set = None

    bind_group_layout: wgpu.BindGroupLayout = None
    bind_group: wgpu.BindGroup = None

    alpha_mode: str = 'BLEND'
    base_color_factor: tuple = (1, 1, 1, 1)

    metallic_factor: float = 0
    roughness_factor: float = 0
    occlusion_strength: float = 1
    emissive_factor: tuple = (0, 0, 0)

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

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(2, self.bind_group)
