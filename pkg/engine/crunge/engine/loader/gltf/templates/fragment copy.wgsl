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
  {% else %}
  surface.metallic = material.metallicFactor;
  surface.roughness = clamp(material.roughnessFactor, 0.04, 1.0);
  {% endif %}

  let dielectricSpec = vec3<f32>(0.04);
  surface.f0 = mix(dielectricSpec, surface.albedo, surface.metallic);
  
  {% if material.has_normal_texture %}
  let tbn = mat3x3(input.tangent, input.bitangent, input.normal);
  let normalMap = textureSample(normalTexture, normalSampler, uv).rgb;
  surface.normal = normalize(tbn * ((2.0 * normalMap) - vec3(1.0)));
  {% else %}
  surface.normal = normalize(input.normal);
  {% endif %}

  {% if material.has_occlusion_texture %}
  let occlusionMap = textureSample(occlusionTexture, occlusionSampler, uv);
  surface.ao = mix(1.0, occlusionMap.r, material.occlusionStrength);
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
  surface.transmission = material.transmissionFactor * transmissionMap.r;
  {% else %}
  surface.transmission = material.transmissionFactor;
  {% endif %}

  return surface;
}

fn GetLight(input : VertexOutput) -> Light {
  var light : Light;
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
    let envDir = -reflect(surface.v, surface.normal);
    let envColor = textureSample(environmentTexture, environmentSampler, envDir).rgb;

    // Attenuate reflection by roughness and metallic
    let reflectionStrength = (1.0 - surface.roughness) * surface.metallic;
    let adjustedReflection = envColor * reflectionStrength;

    // Apply fresnel to control edge reflections
    let fresnel = FresnelSchlick(dot(surface.v, surface.normal), surface.f0);
    return adjustedReflection * fresnel;
}
{% endif %}

// Compute transmission UV with simple refraction
fn getTransmissionUV(surface: Surface, screenUv: vec2<f32>) -> vec2<f32> {
    // Simple screen-space distortion based on surface normal
    let refractionStrength = 0.02 * surface.transmission;
    
    // Use the surface normal's XY components to offset the UV
    let screenOffset = surface.normal.xy * refractionStrength;
    
    return clamp(screenUv + screenOffset, vec2<f32>(0.0), vec2<f32>(1.0));
}

// Sample transmission with roughness-based blur and frosted effect
fn sampleTransmissionWithRoughness(surface: Surface, screenUv: vec2<f32>) -> vec3<f32> {
    let transmissionUv = getTransmissionUV(surface, screenUv);
    
    let pixelSize = 1.0 / viewport.size;
    let blurRadius = surface.roughness * 4.0; // Scale blur by roughness
    
    var totalColor = vec3<f32>(0.0);
    var totalWeight = 0.0;
    
    // 9-tap blur pattern for frosted glass effect
    for (var x = -1; x <= 1; x = x + 1) {
        for (var y = -1; y <= 1; y = y + 1) {
            let offset = vec2<f32>(f32(x), f32(y)) * pixelSize * blurRadius;
            let sampleUv = clamp(transmissionUv + offset, vec2<f32>(0.0), vec2<f32>(1.0));
            
            // Gaussian-like weight
            let weight = exp(-0.5 * (f32(x * x + y * y)));
            
            totalColor += textureSample(snapshotTexture, snapshotSampler, sampleUv).rgb * weight;
            totalWeight += weight;
        }
    }
    
    let blurredBackground = totalColor / totalWeight;
    
    // Create frosted effect by mixing with a brightened, desaturated version
    let frostedIntensity = pow(surface.roughness, 2) * 0.3;
    let brightness = dot(blurredBackground, vec3<f32>(0.299, 0.587, 0.114));
    let frostedColor = mix(blurredBackground, vec3<f32>(brightness), frostedIntensity);
    
    return frostedColor;
}

@fragment
fn fs_main(input : VertexOutput, @builtin(front_facing) front_facing: bool) -> @location(0) vec4<f32> {
    var surface = GetSurface(input);
    if (!front_facing) {
      surface.normal = -surface.normal;
    }

    // Calculate screen UV coordinates
    let screenUv = input.position.xy / viewport.size;
    
    // Sample background with roughness-based blur
    let backgroundColor = sampleTransmissionWithRoughness(surface, screenUv);
    
    // Apply transmission effect according to glTF spec
    let transmission = surface.transmission;
    
    // For transmission, we need to mix the base color with the background
    // The transmission factor controls how much background shows through
    let transmittedColor = backgroundColor * surface.baseColor.rgb;
    
    // Mix between opaque surface and transmitted background
    surface.albedo = mix(surface.albedo, transmittedColor, transmission);

    var light = GetLight(input);
    let Lo = lightRadiance(light, surface);

    // Environment reflection
    {% if material.has_environment_texture %}
    let environmentReflection = getEnvironmentReflection(surface);
    {% else %}
    let environmentReflection = vec3<f32>(0.0);
    {% endif %}

    // Ambient lighting scaled by occlusion
    let ambientStrength = 0.1;
    let ambient = surface.albedo * surface.ao * ambientStrength;

    // Combine all components
    let rgb = ambient + Lo + environmentReflection + surface.emissive;

    // Apply gamma correction
    let finalColor = linearToSRGB(rgb);
    
    // For transmission materials, alpha should be affected by transmission
    let finalAlpha = mix(surface.baseColor.a, 1.0 - transmission, transmission);
    
    return vec4<f32>(finalColor, finalAlpha);
}