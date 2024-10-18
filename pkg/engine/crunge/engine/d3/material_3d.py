from crunge import wgpu

from ..resource.material import Material
from ..resource.texture import Texture
#from .bind_group_layout import BindGroupLayout


class Material3D(Material):
    bind_group_layout: wgpu.BindGroupLayout = None
    bind_group: wgpu.BindGroup = None

    #alpha_mode: str = 'BLEND'
    alpha_mode: str = 'OPAQUE'
    alpha_cutoff: float = 0.5
    double_sided: bool = False

    base_color_factor: tuple = (1, 1, 1, 1)

    metallic_factor: float = 0
    roughness_factor: float = 0
    occlusion_strength: float = 1
    emissive_factor: tuple = (0, 0, 0)

    def __init__(self) -> None:
        super().__init__()

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(2, self.bind_group)
