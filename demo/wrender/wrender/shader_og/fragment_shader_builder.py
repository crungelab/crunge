from textwrap import dedent

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..constants import RESERVED_BINDINGS, TEXTURE_BINDING_START
from ..vertex_table import VertexTable
from ..material import Material
from .shader_builder import ShaderBuilder


shader_code_fragment = """
struct Light {
    position: vec3<f32>,
    color: vec3<f32>,
    intensity: f32,
}
@group(0) @binding(1) var<uniform> light : Light;

// Utility function for gamma correction
const GAMMA = 2.200000048;

fn linearToSRGB(linear : vec3<f32>) -> vec3<f32> {
  let INV_GAMMA = (1.0 / GAMMA);
  return pow(linear, vec3<f32>(INV_GAMMA));
}

fn sRGBToLinear(srgb : vec3<f32>) -> vec3<f32> {
  return pow(srgb, vec3<f32>(GAMMA));
}

fn linearSample(texture: texture_2d<f32>, texSampler: sampler, uv: vec2<f32>) -> vec4<f32>
  {
    let color = textureSample(texture, texSampler, uv);
    return vec4<f32>(sRGBToLinear(color.rgb), color.a);
  }

const pi: f32 = 3.141592653589793;

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
    //let ndotv = dot(n, v);
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
fn fs_main(input : VertexOutput) -> @location(0) vec4<f32> {
"""


class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable, material: Material) -> None:
        super().__init__(vertex_table)
        self.material = material

    def build(self) -> wgpu.ShaderModule :
        super().build()
        logger.debug("Building fragment shader")
        material = self.material
        for i, texture in enumerate(material.textures):
            self(f'@group(0) @binding({i*2+TEXTURE_BINDING_START}) var {texture.name}Sampler: sampler;')
            self(f'@group(0) @binding({i*2+TEXTURE_BINDING_START+1}) var {texture.name}Texture : texture_2d<f32>;')

        self(shader_code_fragment)

        bcf = material.base_color_factor
        with self:
            self(f'let bcf = vec4<f32>({bcf[0]}, {bcf[1]}, {bcf[2]}, {bcf[3]});')

            if self.vertex_table.has('uv'):
                self("let uv = input.uv;")

            if self.vertex_table.has('color'):
                self("let albedo = input.color;")
            elif material.has_texture('baseColor'):
                self(f'let albedo = bcf * linearSample(baseColorTexture, baseColorSampler, uv);')
            else:
                self("let albedo = vec4(1.0, 1.0, 1.0, 1.0);")


            # Metallic
            self(f'let metallic_factor: f32 = {material.metallic_factor};')
            self(f'let roughness_factor: f32 = {material.roughness_factor};')

            if material.has_texture('metallicRoughness'):
                # Its green channel contains roughness values and its blue channel contains metalness values.
                self("""
    let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
    let metallic = metallic_factor * metalRough.b;
    let roughness = clamp(roughness_factor * metalRough.g, 0.04, 1.0);
                """)

            # Normal
            if material.has_texture('normal'):
                self(f'''
    let tbn = mat3x3(input.tangent, input.bitangent, input.normal);
    let normalMap = textureSample(normalTexture, normalSampler, uv).rgb;
    let normal = normalize((tbn * ((2.0 * normalMap) - vec3(1.0))));
    //var normal = textureSample(normalTexture, normalSampler, uv).rgb;
    //normal = normal * 2.0 - 1.0; // Remap from [0, 1] to [-1, 1]
    //normal = normalize(normal.x * input.tangent + normal.y * input.bitangent + normal.z * input.normal);
                '''
                )
            else:
                self('let normal = normalize(input.normal);')
                #self('let normal = input.normal;')

            # Occlusion
            if material.has_texture('occlusion'):
                # The red channel of the texture encodes the occlusion value
                self(f'''let ao = textureSample(occlusionTexture, occlusionSampler, uv).r;'''
                )
            else:
                self('let ao = 1.0;')


            # Emission
            e = material.emissive_factor
            self(f'let emissive_factor = vec3<f32>({e[0]}, {e[1]}, {e[2]});')

            if material.has_texture('emissive'):
                self(f'''let emissive = emissive_factor * textureSample(emissiveTexture, emissiveSampler, uv).rgb;'''
                )
            else:
                self('let emissive = emissive_factor;')

            #self('return color;')
            
            self("""
    let fragPos = input.frag_pos;

    let lightPos = light.position;
    //let lightPos = vec3<f32>(2.0, 2.0, 2.0);
    let lightDir = normalize(lightPos - fragPos);

    let cameraPos = camera.position;
    //let cameraPos = vec3<f32>(0.0, 0.0, 3.0);
    let viewDir = normalize(cameraPos - fragPos);
    //let viewDir = normalize(vec3<f32>(0.0, 0.0, 1.0));
                     
    //let lightColor = light.color * light.intensity;
    let lightColor = light.color * 5.0;
            """)

            if material.has_texture('metallicRoughness'):
                self("""
    let reflection = brdf(albedo.rgb, metallic, roughness, lightDir, viewDir, normal);
    let rgb = reflection * lightColor * ao + emissive;
    let finalColor = linearToSRGB(rgb);
    return vec4<f32>(finalColor, albedo.a);
                """)
            else:
                self("""
    let rgb = albedo.rgb * lightColor * ao;
    let finalColor = linearToSRGB(rgb);
    return vec4<f32>(finalColor, albedo.a);
                """)
            
        self('}')

        logger.debug(f"fragment_shader_code:\n{self.shader_code}")

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        #exit()
        return shader_module
