from crunge.core import klass
from crunge import wgpu
from ...resource.sampler import Sampler

@klass.singleton
class SpriteSampler(Sampler):
    def __init__(self) -> None:

        sampler_desc = wgpu.SamplerDescriptor(
            min_filter=wgpu.FilterMode.LINEAR,
            mag_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_w=wgpu.AddressMode.CLAMP_TO_EDGE,
            max_anisotropy=1,
        )

        #sampler = self.device.create_sampler()
        sampler = self.device.create_sampler(sampler_desc)

        super().__init__(sampler)

