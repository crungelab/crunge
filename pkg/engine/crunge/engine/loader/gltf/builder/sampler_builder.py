from loguru import logger
import numpy as np

from crunge import wgpu
from crunge import gltf

from ....resource import Sampler

from . import GltfBuilder
from .builder_context import BuilderContext

min_filter_map = {
    gltf.TextureFilter.NEAREST: wgpu.FilterMode.NEAREST,
    gltf.TextureFilter.LINEAR: wgpu.FilterMode.LINEAR,
    gltf.TextureFilter.NEAREST_MIPMAP_NEAREST: wgpu.FilterMode.NEAREST,
    gltf.TextureFilter.LINEAR_MIPMAP_NEAREST: wgpu.FilterMode.LINEAR,
    gltf.TextureFilter.NEAREST_MIPMAP_LINEAR: wgpu.FilterMode.NEAREST,
    gltf.TextureFilter.LINEAR_MIPMAP_LINEAR: wgpu.FilterMode.LINEAR,
}

mag_filter_map = {
    gltf.TextureFilter.NEAREST: wgpu.FilterMode.NEAREST,
    gltf.TextureFilter.LINEAR: wgpu.FilterMode.LINEAR,
}

wrap_s_map = {
    gltf.TextureWrap.CLAMP_TO_EDGE: wgpu.AddressMode.CLAMP_TO_EDGE,
    gltf.TextureWrap.MIRRORED_REPEAT: wgpu.AddressMode.MIRROR_REPEAT,
    gltf.TextureWrap.REPEAT: wgpu.AddressMode.REPEAT,
}
wrap_t_map = wrap_s_map  # Assuming wrap_t is the same as wrap_s for simplicity

class SamplerBuilder(GltfBuilder):
    def __init__(
        self, context: BuilderContext,  sampler_index: int
    ) -> None:
        super().__init__(context)
        self.sampler_index = sampler_index

    def build(self) -> Sampler:
        if self.sampler_index in self.context.sampler_cache:
            return self.context.sampler_cache[self.sampler_index]

        tf_sampler = self.tf_model.samplers[self.sampler_index] if self.sampler_index >= 0 else None

        #logger.debug(f"Building Sampler: {tf_sampler.name} (index: {self.sampler_index})")

        address_mode_u = wrap_s_map[tf_sampler.wrap_s] if tf_sampler else wgpu.AddressMode.REPEAT
        address_mode_v = wrap_t_map[tf_sampler.wrap_t] if tf_sampler else wgpu.AddressMode.REPEAT
        # Default to LINEAR for min and mag filters if not specified
        min_filter = min_filter_map.get(tf_sampler.min_filter, wgpu.FilterMode.LINEAR) if tf_sampler else wgpu.FilterMode.LINEAR
        mag_filter = mag_filter_map.get(tf_sampler.mag_filter, wgpu.FilterMode.LINEAR) if tf_sampler else wgpu.FilterMode.LINEAR

        sampler_desc = wgpu.SamplerDescriptor(
            address_mode_u=address_mode_u,
            address_mode_v=address_mode_v,
            #address_mode_w=wgpu.AddressMode.REPEAT,  # Assuming 2D texture, so W is not used
            min_filter=min_filter,
            mag_filter=mag_filter,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            lod_min_clamp=0,
            lod_max_clamp=100,
            #compare=wgpu.CompareFunction.UNDEFINED,
            #max_anisotropy=16,  # Optional, can be set if needed
        )                             

        sampler = Sampler(self.gfx.device.create_sampler(sampler_desc))
        self.context.sampler_cache[self.sampler_index] = sampler
        return sampler
