from textwrap import dedent

from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

from ..vertex_table import VertexTable
from ..material import Material
from .shader_builder import ShaderBuilder


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
"""
#    let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);


class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable, material: Material) -> None:
        super().__init__(vertex_table)
        self.material = material

    def build(self) -> wgpu.ShaderModule :
        super().build()
        logger.debug("Building fragment shader")
        material = self.material
        for i, texture in enumerate(material.textures):
            self(f'@group(0) @binding({i*2+1}) var {texture.name}Sampler: sampler;')
            self(f'@group(0) @binding({i*2+2}) var {texture.name}Texture : texture_2d<f32>;')

        self(shader_code_fragment)
        if self.vertex_table.has('uv'):
            self.write_indented("    let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);\n")

        with self:
            bcf = material.base_color_factor
            self(f'var color = vec4<f32>({bcf[0]}, {bcf[1]}, {bcf[2]}, {bcf[3]});')

            if material.has_texture('baseColor'):
                #self(f'color = color * linearSample(baseColorTexture, baseColorSampler, uv);')
                self(f'color = color * textureSample(baseColorTexture, baseColorSampler, uv);')

            # Metallic
            self(f'var metallic: f32 = {material.metallic_factor};')
            self(f'var roughness: f32 = {material.roughness_factor};')

            if material.has_texture('metallicRoughness'):
                '''
                self("""
    let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv).rg;
    metallic = metallic * metalRough.g;
    roughness = roughness * metalRough.r;
                """)
                '''
                self("""
    let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
    metallic = metallic * metalRough.b;
    roughness = roughness * metalRough.g;
                """)

            self('roughness = clamp(roughness, 0.04, 1.0);')

            # Normal
            if material.has_texture('normal'):
                self(f'''
    var normal = textureSample(normalTexture, normalSampler, uv).rgb;
    normal = normal * 2.0 - 1.0;
    normal = normalize(normal);
                '''
                )
            else:
                self('var normal = normalize(in.normal);')

            # Occlusion
            if material.has_texture('occlusion'):
                self(f'''var ao = textureSample(occlusionTexture, occlusionSampler, uv).r;'''
                )
            else:
                self('let ao = 1.0;')


            # Emission
            e = material.emissive_factor
            self(f'var emissive = vec3<f32>({e[0]}, {e[1]}, {e[2]});')

            if material.has_texture('emissive'):
                self(f'''emissive = emissive * textureSample(emissiveTexture, emissiveSampler, uv).rgb;'''
                )

            self("""
    let lightDir = normalize(vec3<f32>(2.0, 4.0, 3.0));
    let viewDir = normalize(vec3<f32>(0.0, 0.0, 1.0));
    var rgb = brdf(color.rgb, metallic, roughness, lightDir, viewDir, normal) * ao + emissive;
    rgb = pow(rgb, vec3<f32>(1.0 / 2.2));
    return vec4<f32>(rgb, color.a);
            """)

        self('}')

        #logger.debug(f"fragment_shader_code:\n{self.shader_code}")

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        #exit()
        return shader_module
