from loguru import logger
import numpy as np
import trimesh as tm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..material import Material
from .shader_builder import ShaderBuilder


shader_code_header = """
struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@group(0) @binding(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

"""

shader_code_footer = """

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
  return textureSample(baseColorTexture, baseColorSampler, uv);
}
"""


class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self) -> None:
        super().__init__(shader_code_header)

    def build(self, material: Material) -> wgpu.ShaderModule :
        for i, texture in enumerate(material.textures):
            self(f'@group(0) @binding({i*2+1}) var {texture.name}Sampler: sampler;')
            self(f'@group(0) @binding({i*2+2}) var {texture.name}Texture : texture_2d<f32>;')

        self(shader_code_footer)

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        return shader_module
