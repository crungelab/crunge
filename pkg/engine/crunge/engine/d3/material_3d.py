from crunge import wgpu

from ..resource import Texture, Material


class Material3D(Material):
    def __init__(self) -> None:
        super().__init__()
        self.textures: list[Texture] = []
        self.texture_set: set = set()

        self.bind_group_layout: wgpu.BindGroupLayout = None
        self.bind_group: wgpu.BindGroup = None

        self.alpha_mode: str = "OPAQUE"
        self.alpha_cutoff: float = 0.5
        self.double_sided: bool = False

        self.base_color_factor: tuple = (1, 1, 1, 1)

        self.metallic_factor: float = 0
        self.roughness_factor: float = 0
        self.occlusion_strength: float = 1
        self.emissive_factor: tuple = (0, 0, 0)

    def add_texture(self, texture: Texture):
        if texture.name in self.texture_set:
            return
        self.textures.append(texture)
        self.texture_set.add(texture.name)

    def has_texture(self, name: str) -> bool:
        return name in self.texture_set

    @property
    def has_base_color_texture(self):
        return self.has_texture("baseColor")

    @property
    def has_metallic_roughness_texture(self):
        return self.has_texture("metallicRoughness")

    @property
    def has_normal_texture(self):
        return self.has_texture("normal")

    @property
    def has_occlusion_texture(self):
        return self.has_texture("occlusion")

    @property
    def has_emissive_texture(self):
        return self.has_texture("emissive")

    @property
    def has_environment_texture(self):
        return self.has_texture("environment")

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(2, self.bind_group)
