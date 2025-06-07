from loguru import logger
import numpy as np

from crunge import wgpu
from crunge import gltf

from ....resource import Sampler

from . import GltfBuilder
from .builder_context import BuilderContext

'''
.def_readwrite("name", &tinygltf::Sampler::name)
.def_readwrite("min_filter", &tinygltf::Sampler::minFilter)
.def_readwrite("mag_filter", &tinygltf::Sampler::magFilter)
.def_readwrite("wrap_s", &tinygltf::Sampler::wrapS)
.def_readwrite("wrap_t", &tinygltf::Sampler::wrapT)
.def_readwrite("extras", &tinygltf::Sampler::extras)
.def_readwrite("extensions", &tinygltf::Sampler::extensions)
.def_readwrite("extras_json_string", &tinygltf::Sampler::extras_json_string)
.def_readwrite("extensions_json_string", &tinygltf::Sampler::extensions_json_string)
'''

'''
class TextureFilter:
    NEAREST = 9728
    LINEAR = 9729
    NEAREST_MIPMAP_NEAREST = 9984
    LINEAR_MIPMAP_NEAREST = 9985
    NEAREST_MIPMAP_LINEAR = 9986
    LINEAR_MIPMAP_LINEAR = 9987
'''

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

'''
class TextureWrap:
    REPEAT = 10497
    CLAMP_TO_EDGE = 33071
    MIRRORED_REPEAT = 33648
'''

'''
py::enum_<AddressMode>(m, "AddressMode", py::arithmetic())
    .value("UNDEFINED", AddressMode::Undefined)
    .value("CLAMP_TO_EDGE", AddressMode::ClampToEdge)
    .value("REPEAT", AddressMode::Repeat)
    .value("MIRROR_REPEAT", AddressMode::MirrorRepeat)
;
'''

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

        tf_sampler = self.tf_model.samplers[self.sampler_index]

        logger.debug(f"Building Sampler: {tf_sampler.name} (index: {self.sampler_index})")

        sampler_desc = wgpu.SamplerDescriptor(
            #address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_u=wrap_s_map.get(tf_sampler.wrap_s, wgpu.AddressMode.REPEAT),
            #address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_v=wrap_t_map.get(tf_sampler.wrap_t, wgpu.AddressMode.REPEAT),
            #address_mode_w=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,  # Assuming 2D texture, so W is not used
            #min_filter=wgpu.FilterMode.LINEAR,
            min_filter=min_filter_map.get(tf_sampler.min_filter, wgpu.FilterMode.LINEAR),
            #mag_filter=wgpu.FilterMode.LINEAR,
            mag_filter=mag_filter_map.get(tf_sampler.mag_filter, wgpu.FilterMode.LINEAR),
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            lod_min_clamp=0,
            lod_max_clamp=100,
            compare=wgpu.CompareFunction.UNDEFINED,
            max_anisotropy=16,
        )

        sampler = Sampler(self.gfx.device.create_sampler(sampler_desc))

        #sampler = None
        self.context.sampler_cache[self.sampler_index] = sampler
        return sampler
