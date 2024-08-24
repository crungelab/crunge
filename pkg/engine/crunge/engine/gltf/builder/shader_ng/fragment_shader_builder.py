from textwrap import dedent

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine.material import Material

from ...constants import TEXTURE_BINDING_START

from ..vertex_table import VertexTable
from ..builder_context import BuilderContext

from .shader_builder import ShaderBuilder


shader_code_fragment = """
struct AmbientLight {
    color: vec3<f32>,
    energy: f32,
}
@group(0) @binding(1) var<uniform> ambientLight : AmbientLight;

struct Light {
    position: vec3<f32>,
    color: vec3<f32>,
    energy: f32,
}
@group(0) @binding(2) var<uniform> light : Light;

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
    let ndotv = clamp(dot(n, v), 0.0, 1.0);
    let ndoth = clamp(dot(n, h), 0.0, 1.0);
    let vdoth = clamp(dot(v, h), 0.0, 1.0);

    let f0 = vec3<f32>(0.04);
    let diffuseColor = color * (1.0 - f0) * (1.0 - metallic);
    let specularColor = mix(f0, color, metallic);

    let f = f0 + (specularColor - f0) * pow(1.0 - vdoth, 5.0);

    let r2 = roughness * roughness;
    let r4 = r2 * r2;
    let attenuationL = 2.0 * ndotl / (ndotl + sqrt(r4 + (1.0 - r4) * ndotl * ndotl));
    let attenuationV = 2.0 * ndotv / (ndotv + sqrt(r4 + (1.0 - r4) * ndotv * ndotv));
    let g = attenuationL * attenuationV;

    let temp = ndoth * ndoth * (r2 - 1.0) + 1.0;
    let d = r2 / (pi * temp * temp);

    //let diffuse = (1.0 - f) / pi * diffuseColor;
    let diffuse = (1.0 - metallic) * (1.0 - f) / pi * diffuseColor;
    let specular = max(f * g * d / (4.0 * ndotl * ndotv), vec3<f32>(0.0));
    return ndotl * (diffuse + specular) * 2.0 + color * 0.1;
}

// Convert a reflection vector to equirectangular coordinates
fn reflectionToEquirectangularUV(normal: vec3<f32>, viewDir: vec3<f32>) -> vec2<f32> {
    let reflection = normalize(reflect(viewDir, normal));

    // Calculate spherical coordinates
    let theta = atan2(reflection.z, reflection.x); // Longitude [-π, π]
    let phi = asin(reflection.y);                  // Latitude [-π/2, π/2]

    // Map spherical coordinates to texture coordinates
    let u = (theta / (2.0 * pi)) + 0.5;
    let v = (phi / pi) + 0.5;

    return vec2<f32>(u, v);
}

@fragment
fn fs_main(input : VertexOutput) -> @location(0) vec4<f32> {
"""


class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable, material: Material) -> None:
        super().__init__(context, vertex_table)
        self.material = material

    def build(self) -> wgpu.ShaderModule :
        super().build()
        logger.debug("Building fragment shader")
        material = self.material
        for i, texture in enumerate(material.textures):
            self.out(f"@group(0) @binding({i*2+TEXTURE_BINDING_START}) var {texture.name}Sampler: sampler;")
            self.out(f"@group(0) @binding({i*2+TEXTURE_BINDING_START+1}) var {texture.name}Texture : texture_2d<f32>;")

        self.out(shader_code_fragment)

        bcf = material.base_color_factor
        with self.out:
            self.out(f"let bcf = vec4<f32>({bcf[0]}, {bcf[1]}, {bcf[2]}, {bcf[3]});")

            if self.vertex_table.has('uv'):
                self.out("let uv = input.uv;")

            if self.vertex_table.has('color'):
                self.out("let albedo = bcf * input.color;")
            elif material.has_texture('baseColor'):
                self.out("let albedo = bcf * linearSample(baseColorTexture, baseColorSampler, uv);")
            else:
                self.out("let albedo = bcf;")


            # Metallic
            self.out(f"let metallicFactor: f32 = {material.metallic_factor};")
            self.out(f"let roughnessFactor: f32 = {material.roughness_factor};")

            if material.has_texture("metallicRoughness"):
                # Its green channel contains roughness values and its blue channel contains metalness values.
                self.out("""
                let metallicRoughness = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
                let metallic = metallicFactor * metallicRoughness.b;
                //let roughness = clamp(roughnessFactor * metallicRoughness.g, 0.04, 1.0);
                let roughness = roughnessFactor * metallicRoughness.g;
                """)
            else:
                self.out("let metallic = metallicFactor;")
                self.out("let roughness = roughnessFactor;")

            # Normal
            if material.has_texture("normal"):
                self.out("""
                let tbn = mat3x3(input.tangent, input.bitangent, input.normal);
                let normalMap = textureSample(normalTexture, normalSampler, uv).rgb;
                let normal = normalize((tbn * ((2.0 * normalMap) - vec3(1.0))));
                //let normal = tbn * ((2.0 * normalMap) - vec3(1.0));
                """)
            else:
                self.out("let normal = input.normal;")

            # Occlusion
            if material.has_texture("occlusion"):
                # The red channel of the texture encodes the occlusion value
                self.out("let ao = textureSample(occlusionTexture, occlusionSampler, uv).r;")
            else:
                self.out("let ao = 1.0;")


            # Emission
            e = material.emissive_factor
            self.out(f"let emissive_factor = vec3<f32>({e[0]}, {e[1]}, {e[2]});")

            if material.has_texture("emissive"):
                self.out("let emissive = emissive_factor * textureSample(emissiveTexture, emissiveSampler, uv).rgb;")
            else:
                self.out("let emissive = emissive_factor;")
            
            self.out("""
            let fragPos = input.frag_pos;

            let lightPos = light.position;
            let lightDir = normalize(lightPos - fragPos);
            //let lightDir = normalize(fragPos - lightPos);

            let cameraPos = camera.position;
            let viewDir = normalize(cameraPos - fragPos);
            //let viewDir = normalize(fragPos - cameraPos);
                                                 
            //let lightColor = light.color * light.energy;
            let lightColor = light.color * 5.0;
            let reflection = brdf(albedo.rgb, metallic, roughness, lightDir, -viewDir, normal);
            """)

            if material.has_texture("environment"):
                self.out("""
                let envUv = reflectionToEquirectangularUV(normal, -viewDir);
                let envColor = textureSample(environmentTexture, environmentSampler, envUv).rgb;
                // Adjust environment contribution based on roughness
                let envRoughness = mix(1.0, 0.0, roughness);
                let envContribution = envColor * envRoughness;

                // Combine direct and indirect lighting
                let diffuseColor = mix(albedo.rgb, vec3(0.0), metallic);
                let specularColor = mix(vec3(0.04), albedo.rgb, metallic);

                let ambient = 
                    (diffuseColor * envContribution * metallic) +
                    (specularColor * envContribution);
                """)
            else:
                self.out("""
                //let ambient = vec3<f32>(0.3) * albedo.rgb;
                let ambient = albedo.rgb;
                """)

            self.out("""
            //let rgb = ambient * ao + emissive;
            let rgb = ambient * ao + emissive + (reflection * lightColor * .25);
            //let rgb = (reflection * lightColor);
            let finalColor = linearToSRGB(rgb);
            return vec4<f32>(finalColor, albedo.a);
            """)

        self.out("}")

        #logger.debug(f"fragment_shader_code:\n{self.shader_code}")

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        #exit()
        return shader_module
