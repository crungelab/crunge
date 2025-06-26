{% include '_viewport.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_model.wgsl' %}
{% include '_light.wgsl' %}
{% include '_lighting.wgsl' %}
{% include '_environment.wgsl' %}
{% include '_bindings.wgsl' %}
{% include '_vertex_output.wgsl' %}

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
  alphaCutoff : f32,
  transmissionFactor : f32,
}

fn GetMaterial() -> Material {
  var material : Material;
  material.baseColorFactor = vec4<f32>({{ base_color_factor[0] }}, {{ base_color_factor[1] }}, {{ base_color_factor[2] }}, {{ base_color_factor[3] }});
  material.emissiveFactor = vec3<f32>({{ emissive_factor[0] }}, {{ emissive_factor[1] }}, {{ emissive_factor[2] }});
  material.occlusionStrength = {{ occlusion_strength }};
  material.metallicFactor = {{ metallic_factor }};
  material.roughnessFactor = {{ roughness_factor }};
  material.alphaCutoff = {{ alpha_cutoff }};
  material.transmissionFactor = {{ transmission_factor }};

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
  transmission: f32,
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

  {%if alpha_mode == 'MASK' %}
  if (surface.baseColor.a < material.alphaCutoff) {
    discard;
  }
  {% endif %}

  surface.albedo = surface.baseColor.rgb;

  {% if material.has_metallic_roughness_texture %}
  let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
  surface.metallic = material.metallicFactor * metalRough.b;
  surface.roughness = clamp(material.roughnessFactor * metalRough.g, 0.04, 1.0);
  //surface.roughness = material.roughnessFactor * metalRough.g;

  {% else %}
  surface.metallic = material.metallicFactor;
  surface.roughness = material.roughnessFactor;
  {% endif %}

  let dielectricSpec = vec3<f32>(0.039999999);
  surface.f0 = mix(dielectricSpec, surface.albedo, surface.metallic);
  

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

  {% if material.has_transmission_texture %}
  let transmissionMap = textureSample(transmissionTexture, transmissionSampler, uv);
  surface.transmission = (material.transmissionFactor * transmissionMap.r);
  {% else %}
  surface.transmission = material.transmissionFactor;
  {% endif %}

  return surface;
}

fn GetLight(input : VertexOutput) -> Light {
  var light : Light;
  //light.kind = LightKind_Spot;
  //light.kind = LightKind_Directional;
  light.kind = LightKind_Point;
  light.position = lightUniform.position;
  light.v = light.position - input.frag_pos;
  light.color = lightUniform.color;
  light.energy = lightUniform.energy;
  light.range = lightUniform.range;
  return light;
}

{% if material.has_environment_texture %}
fn getEnvironmentReflection(surface: Surface) -> vec3<f32> {
    let envDir = normalize(-reflect(surface.v, surface.normal));
    let envColor = textureSample(environmentTexture, environmentSampler, envDir).rgb;

    // Attenuate reflection by roughness (rough surfaces should be less reflective)
    let reflectionStrength = (1.0 - surface.roughness) * surface.metallic;

    // Further scale the environment reflection to control shininess
    let adjustedReflection = envColor * reflectionStrength;

    // Apply fresnel to control edge reflections
    let fresnel = FresnelSchlick(dot(surface.v, surface.normal), surface.f0);
    return adjustedReflection * fresnel;
}
{% endif %}

// ... (keep all previous helper functions, structs, and includes) ...

@fragment
fn fs_main(input : VertexOutput, @builtin(front_facing) is_front: bool) -> @location(0) vec4<f32> {
    var surface = GetSurface(input);
    var light = GetLight(input);

    // --- 1. Fix for Two-Sided Rendering ---
    if (!is_front) {
        surface.normal = -surface.normal;
    }

    // --- 2. Implement the Layered BRDF Formula ---

    // The formula is: fresnel_mix(layer, base)
    // We will calculate the 'layer' and 'base' components first.

    // A) Calculate the 'layer' component: specular_brdf()
    // This is the total specular reflection from all light sources. We will use the
    // existing lighting functions to get this.
    let directLighting = lightRadiance(light, surface);
    {% if material.has_environment_texture %}
    let indirectLighting = getEnvironmentReflection(surface);
    {% else %}
    let indirectLighting = vec3<f32>(0.0);
    {% endif %}
    // 'layer' represents the total reflected light from an equivalent opaque surface.
    let layer = directLighting + indirectLighting;


    // B) Calculate the 'base' component: mix(diffuse_brdf, specular_btdf * baseColor, transmission)
    // This component represents the light that enters the surface.

    // B.1 - The diffuse part of the base (for when transmission is 0).
    // We'll use a simple ambient term for this, as the direct lighting is already
    // part of the 'layer' reflection. This prevents double-counting light.
    let ambient = (surface.albedo * 0.1) * surface.ao;
    let diffuse_base = ambient;

    // B.2 - The transmissive part of the base (for when transmission is 1).
    // This implements the `specular_btdf` by blurring the background based on roughness.
    let snapshotUv = input.position.xy / viewport.size;

    // For rough transmission ("frosted glass"), we sample a higher mip level of the
    // background texture. NOTE: This requires your `snapshotTexture` to have mipmaps.
    const MAX_MIP_LEVEL = 8.0; // Adjust based on your snapshot texture's mip count.
    let mipLevel = surface.roughness * surface.roughness * MAX_MIP_LEVEL; // Squaring roughness gives a more perceptual result
    let backgroundColor = textureSampleLevel(snapshotTexture, snapshotSampler, snapshotUv, mipLevel).rgb;
    
    // The transmitted light is tinted by the material's color.
    let transmissive_base = backgroundColor * surface.albedo;

    // B.3 - Mix the diffuse and transmissive parts to get the final 'base' color.
    let base = mix(diffuse_base, transmissive_base, surface.transmission);


    // C) Combine 'layer' and 'base' using fresnel_mix
    // The final color is `base * (1 - F) + layer * F`, where F is the Fresnel term.
    let fresnel = FresnelSchlick(max(dot(surface.normal, surface.v), 0.0), surface.f0);
    let finalLinearColor = base * (vec3<f32>(1.0) - fresnel) + layer * fresnel;


    // --- 3. Final Output ---
    let finalColorWithEmission = finalLinearColor + surface.emissive;
    let finalSrgbColor = linearToSRGB(finalColorWithEmission);
    let finalAlpha = surface.baseColor.a;

    return vec4<f32>(finalSrgbColor, finalAlpha);
}