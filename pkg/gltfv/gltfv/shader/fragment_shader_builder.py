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

shader_code_fragment = """

fn linearSample(texture: texture_2d<f32>, texSampler: sampler, uv: vec2<f32>) -> vec4<f32>
  {
    let color = textureSample(texture, texSampler, uv);
    return vec4<f32>(pow(color.rgb, vec3<f32>(2.2)), color.a);
  }

const pi: f32 = 3.141592653589793;

fn blinnPhong(color: vec3<f32>,
        l: vec3<f32>,
        v: vec3<f32>,
        n: vec3<f32>) -> vec3<f32>
{
    let specExp = 64.0;
    let intensity = 0.5;
    let ambient = 0.5;

    let diffuse = max(dot(n, l), 0.0);
    let specular = pow(max(dot(n, normalize(l + v)), 0.0), specExp);

    return color * ((diffuse + specular) * intensity + ambient);
}

fn brdf(color: vec3<f32>,
        metallic: f32,
        roughness: f32,
        l: vec3<f32>,
        v: vec3<f32>,
        n: vec3<f32>) -> vec3<f32>
{
    let h = normalize(l + v);
    let ndotl = clamp(dot(n, l), 0.0, 1.0);
    let ndotv = abs(dot(n, v));
    let ndoth = clamp(dot(n, h), 0.0, 1.0);
    let vdoth = clamp(dot(v, h), 0.0, 1.0);

    let f0 = vec3<f32>(0.04);
    let diffuseColor = color * (1.0 - f0) * (1.0 - metallic);
    let specularColor = mix(f0, color, metallic);

    let reflectance = max(max(specularColor.r, specularColor.g), specularColor.b);
    let reflectance0 = specularColor;
    let reflectance9 = vec3<f32>(clamp(reflectance * 25.0, 0.0, 1.0));
    let f = reflectance0 + (reflectance9 - reflectance0) * pow(1.0 - vdoth, 5.0);

    let r2 = roughness * roughness;
    let r4 = r2 * r2;
    let attenuationL = 2.0 * ndotl / (ndotl + sqrt(r4 + (1.0 - r4) * ndotl * ndotl));
    let attenuationV = 2.0 * ndotv / (ndotv + sqrt(r4 + (1.0 - r4) * ndotv * ndotv));
    let g = attenuationL * attenuationV;

    let temp = ndoth * ndoth * (r2 - 1.0) + 1.0;
    let d = r2 / (pi * temp * temp);

    let diffuse = (1.0 - f) / pi * diffuseColor;
    let specular = max(f * g * d / (4.0 * ndotl * ndotv), vec3<f32>(0.0));
    return ndotl * (diffuse + specular) * 2.0 + color * 0.1;
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
"""


class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self) -> None:
        super().__init__(shader_code_header)

    def build(self, material: Material) -> wgpu.ShaderModule :
        for i, texture in enumerate(material.textures):
            self(f'@group(0) @binding({i*2+1}) var {texture.name}Sampler: sampler;')
            self(f'@group(0) @binding({i*2+2}) var {texture.name}Texture : texture_2d<f32>;')

        #self(shader_code_footer)
        #self('@fragment')
        #self('fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {')
        self(shader_code_fragment)
        with self:
            #self('let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);')
            self('let lightDir = normalize(vec3<f32>(2.0, 4.0, 3.0));')
            self(f'var color = vec4<f32>{material.base_color_factor};')
            #self('return textureSample(baseColorTexture, baseColorSampler, uv);')
            if material.base_color_texture:
                #self(f'color = color * linearSample(baseColorTexture, baseColorSampler, uv);')
                self(f'color = color * textureSample(baseColorTexture, baseColorSampler, uv);')

            # Metallic
            self(f'var metallic: f32 = {material.metallic_factor};')
            self(f'var roughness: f32 = {material.roughness_factor};')
            if material.metallic_roughness_texure:
                self('let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);')
                self('metallic = metallic * metalRough.b;')
                self('roughness = roughness * metalRough.g;')
            self('roughness = clamp(roughness, 0.04, 1.0);')

            self('return color;')
            #self("""
            #let viewDir = normalize(camera.eye - worldPos);
            #var rgb = brdf(color.rgb, metallic, roughness, lightDir, viewDir, normal) * ao + emissive;
            #rgb = pow(rgb, vec3<f32>(1.0 / 2.2));
            #return vec4<f32>(rgb, color.a);
            #""")

        self('}')

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        return shader_module
