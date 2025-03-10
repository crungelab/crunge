from crunge.core import klass
from crunge import wgpu
from ...resource.sampler import Sampler

@klass.singleton
class DefaultSpriteSampler(Sampler):
    def __init__(self) -> None:

        sampler_desc = wgpu.SamplerDescriptor(
            #min_filter=wgpu.FilterMode.LINEAR,
            min_filter=wgpu.FilterMode.NEAREST,
            #mag_filter=wgpu.FilterMode.LINEAR,
            mag_filter=wgpu.FilterMode.NEAREST,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_w=wgpu.AddressMode.CLAMP_TO_EDGE,
            max_anisotropy=1,
        )

        sampler = self.device.create_sampler(sampler_desc)

        super().__init__(sampler)


@klass.singleton
class RepeatingSpriteSampler(Sampler):
    def __init__(self) -> None:

        sampler_desc = wgpu.SamplerDescriptor(
            min_filter=wgpu.FilterMode.LINEAR,
            #min_filter=wgpu.FilterMode.NEAREST,
            mag_filter=wgpu.FilterMode.LINEAR,
            #mag_filter=wgpu.FilterMode.NEAREST,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,
            max_anisotropy=1,
        )

        sampler = self.device.create_sampler(sampler_desc)

        super().__init__(sampler)

