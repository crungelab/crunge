{% include '_vertex_output.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_light.wgsl' %}
{% include '_lighting.wgsl' %}
{% include '_environment.wgsl' %}
{% include '_bindings.wgsl' %}

// Utility function for gamma correction
const GAMMA = 2.200000048;

fn linearToSRGB(linear : vec3<f32>) -> vec3<f32> {
  let INV_GAMMA = (1.0 / GAMMA);
  return pow(linear, vec3<f32>(INV_GAMMA));
}

fn sRGBToLinear(srgb : vec3<f32>) -> vec3<f32> {
  return pow(srgb, vec3<f32>(GAMMA));
}

fn linearSample(texture: texture_2d<f32>, texSampler: sampler, uv: vec2<f32>) -> vec4<f32> {
  let color = textureSample(texture, texSampler, uv);
  return vec4<f32>(sRGBToLinear(color.rgb), color.a);
}

const pi: f32 = 3.141592653589793;

struct Material {
  baseColorFactor : vec4<f32>,
  emissiveFactor : vec3<f32>,
  occlusionStrength : f32,
  metallicFactor : f32,
  roughnessFactor : f32,
  //alphaCutoff : f32,
}

fn GetMaterial() -> Material {
  var material : Material;
  material.baseColorFactor = vec4<f32>({{ base_color_factor[0] }}, {{ base_color_factor[1] }}, {{ base_color_factor[2] }}, {{ base_color_factor[3] }});
  material.emissiveFactor = vec3<f32>({{ emissive_factor[0] }}, {{ emissive_factor[1] }}, {{ emissive_factor[2] }});
  material.occlusionStrength = {{ occlusion_strength }};
  material.metallicFactor = {{ metallic_factor }};
  material.roughnessFactor = {{ roughness_factor }};
  //material.alphaCutoff = {{ alpha_cutoff }};
  return material;
}

struct Surface {
  baseColor : vec4<f32>,
  albedo : vec3<f32>,
  metallic : f32,
  roughness : f32,
  position : vec3<f32>,
  normal : vec3<f32>,
  f0 : vec3<f32>,
  ao : f32,
  emissive : vec3<f32>,
  v : vec3<f32>,
  ambient : vec3<f32>,
}

fn GetSurface(input : VertexOutput) -> Surface {
  var surface : Surface;
  var material = GetMaterial();

  surface.position = input.frag_pos;
  surface.v = normalize(camera.position - input.frag_pos);

  {% if vertex_table.has_uv %}
  let uv = input.uv;
  {% endif %}

  {% if vertex_table.has_color %}
  let baseColor = input.color * material.baseColorFactor;
  {% else %}
  let baseColor = material.baseColorFactor;
  {% endif %}

  {% if material.has_base_color_texture %}
  let baseColorMap = linearSample(baseColorTexture, baseColorSampler, uv);
  surface.baseColor = baseColor * baseColorMap;
  {% else %}
  surface.baseColor = baseColor;
  {% endif %}
  surface.albedo = surface.baseColor.rgb;

  {% if material.has_metallic_roughness_texture %}
  let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
  surface.metallic = material.metallicFactor * metalRough.b;
  //surface.roughness = clamp(material.roughnessFactor * metalRough.g, 0.04, 1.0);
  surface.roughness = clamp(material.roughnessFactor * metalRough.g, 0.1, 1.0); // Adjust the lower bound

  {% else %}
  surface.metallic = material.metallicFactor;
  surface.roughness = material.roughnessFactor;
  {% endif %}

  let dielectricSpec = vec3(0.039999999);
  surface.f0 = mix(dielectricSpec, surface.albedo, vec3(surface.metallic));

  {% if material.has_normal_texture %}
  let tbn = mat3x3(input.tangent, input.bitangent, input.normal);
  let normalMap = textureSample(normalTexture, normalSampler, uv).rgb;
  surface.normal = normalize((tbn * ((2.0 * normalMap) - vec3(1.0))));
  {% else %}
  surface.normal = normalize(input.normal);
  //surface.normal = input.normal;
  {% endif %}

  {% if material.has_occlusion_texture %}
  let occlusionMap = textureSample(occlusionTexture, occlusionSampler, uv);
  surface.ao = (material.occlusionStrength * occlusionMap.r);
  {% else %}
  surface.ao = 1.0;
  {% endif %}

  {% if material.has_emissive_texture %}
  surface.emissive = material.emissiveFactor * textureSample(emissiveTexture, emissiveSampler, uv).rgb;
  {% else %}
  surface.emissive = material.emissiveFactor;
  {% endif %}

  {% if material.has_environment_texture %}
  let envDir = normalize(-reflect(surface.v, surface.normal));
  //let envUv = directionToEquirectangularUV(envDir);
  //surface.environment = textureSample(environmentTexture, environmentSampler, envUv).rgb;
  //let envColor = textureSample(environmentTexture, environmentSampler, envUv).rgb;
  let envColor = textureSample(environmentTexture, environmentSampler, envDir).rgb;

  // Adjust environment contribution based on roughness
  let envRoughness = mix(1.0, 0.0, surface.roughness);
  let envContribution = envColor * envRoughness;

  // Combine direct and indirect lighting
  let diffuseColor = mix(surface.albedo, vec3(0.0), surface.metallic);
  let specularColor = mix(vec3(0.04), surface.albedo, surface.metallic);

  surface.ambient =
      ((diffuseColor * envContribution * surface.metallic) +
      (specularColor * envContribution));

  /*
  let envRoughness = mix(0.5, 1.0, surface.roughness); // Adjust this mix to reduce shine
  let envContribution = envColor * envRoughness;

  let diffuseColor = mix(surface.albedo, vec3(0.0), surface.metallic);
  let specularColor = mix(vec3(0.04), surface.albedo, surface.metallic) * envRoughness;

  surface.ambient = ((diffuseColor * envContribution * (1.0 - surface.metallic)) +
                    (specularColor * envContribution));
  */

  {% else %}
  surface.ambient = surface.albedo;
  {% endif %}

  return surface;
}

fn GetLight(input : VertexOutput) -> Light {
  var light : Light;
  //light.kind = LightKind_Spot;
  //light.kind = LightKind_Directional;
  light.kind = LightKind_Point;
  //light.v = normalize(lightUniform.position - input.frag_pos);
  light.v = lightUniform.position - input.frag_pos;
  //light.color = lightUniform.color;
  light.color = vec3<f32>(1.0, 1.0, 1.0);
  //light.range = lightUniform.range;
  light.range = 10.0;
  //light.energy = lightUniform.energy;
  light.energy = 10.0;
  return light;
}

@fragment
fn fs_main(input : VertexOutput) -> @location(0) vec4<f32> {
  var surface = GetSurface(input);
  var light = GetLight(input);

  // Calculate Fresnel factor
  let fresnelFactor = pow(1.0 - dot(surface.v, surface.normal), 5.0);
  let fresnel = mix(surface.f0, vec3(1.0), fresnelFactor);

  let reflection = lightRadiance(light, surface) * fresnel;
  let ambient = surface.ambient * surface.ao;
  let rgb = reflection + ambient + surface.emissive;
  let finalColor = linearToSRGB(rgb);
  return vec4<f32>(finalColor, surface.baseColor.a);             
}