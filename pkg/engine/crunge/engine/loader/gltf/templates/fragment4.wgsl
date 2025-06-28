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

@fragment
fn fs_main(input : VertexOutput, @builtin(front_facing) front_facing: bool) -> @location(0) vec4<f32> {
    var surface = GetSurface(input);
    if (!front_facing) {
      surface.normal = -surface.normal;
    }

    var light = GetLight(input);

    // --- 1. Calculate Lighting Contributions ---

    // Calculate direct lighting (from point/spot/directional lights).
    // This typically includes both diffuse and specular components from the BRDF.
    let directLighting = lightRadiance(light, surface);

    // Calculate indirect lighting (reflections from the environment map).
    {% if material.has_environment_texture %}
    let indirectLighting = getEnvironmentReflection(surface);
    {% else %}
    let indirectLighting = vec3<f32>(0.0);
    {% endif %}

    // Combine all potential reflected light. This is what would be reflected
    // by a fully opaque version of the material.
    let totalReflectedLight = directLighting + indirectLighting;


    // --- 2. Define Opaque vs. Transmissive Appearance ---

    // The final color is a mix between a fully opaque and a fully transmissive
    // version of the material, controlled by `surface.transmission`.

    // A) Define the appearance if the material is fully OPAQUE.
    // This is standard PBR shading: ambient occlusion + total reflection + emission.
    let ambientStrength = 0.1;
    let opaqueComponent = (surface.albedo * ambientStrength) * surface.ao + totalReflectedLight + surface.emissive;

    // B) Define the appearance if the material is fully TRANSMISSIVE.
    // This involves light passing through the object from behind.

    // Get the color of the scene behind the fragment using screen-space UVs.
    let snapshotUv = input.position.xy / viewport.size;
    let backgroundColor = textureSample(snapshotTexture, snapshotSampler, snapshotUv).rgb;

    // The light passing through the object is tinted by the surface's color (albedo).
    let transmittedLight = backgroundColor * surface.albedo;

    // A transmissive surface still has specular reflections. The ratio of reflection
    // to transmission depends on the viewing angle, an effect modeled by the Fresnel equations.
    let n = surface.normal;
    let v = surface.v;
    let f0 = surface.f0;
    let fresnel = FresnelSchlick(max(dot(n, v), 0.0), f0);

    // The final color for the transmissive surface is a mix of the light that reflects
    // and the light that passes through. The `fresnel` term is the mixing factor.
    // Correct formulation: mix(light_that_passes_through, light_that_reflects, reflection_ratio)
    let transmissiveComponent = mix(transmittedLight, totalReflectedLight, fresnel);
    

    // --- 3. Final Color Calculation ---

    // Blend between the opaque and transmissive appearances using the material's transmission factor.
    let mixedColor = mix(opaqueComponent, transmissiveComponent, surface.transmission);

    // Apply gamma correction for display.
    let finalColor = linearToSRGB(mixedColor);

    // For proper blending by the GPU, the final alpha should also be affected by transmission.
    // A fully transmissive material should have its color determined by what's behind it,
    // which corresponds to an effective alpha of 0.
    let finalAlpha = surface.baseColor.a * (1.0 - surface.transmission);
    //let finalAlpha = surface.baseColor.a;

    return vec4<f32>(finalColor, finalAlpha);
}