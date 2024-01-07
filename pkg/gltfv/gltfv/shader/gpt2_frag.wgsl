@group(0) @binding(1) var baseColorSampler: sampler;
@group(0) @binding(2) var baseColorTexture: texture_2d<f32>;
@group(0) @binding(3) var metallicRoughnessSampler: sampler;
@group(0) @binding(4) var metallicRoughnessTexture: texture_2d<f32>;
@group(0) @binding(5) var normalSampler: sampler;
@group(0) @binding(6) var normalTexture: texture_2d<f32>;
@group(0) @binding(7) var occlusionSampler: sampler;
@group(0) @binding(8) var occlusionTexture: texture_2d<f32>;
@group(0) @binding(9) var emissiveSampler: sampler;
@group(0) @binding(10) var emissiveTexture: texture_2d<f32>;

// ... [Other functions like linearSample, brdf, etc., remain the same]

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let uv = in.uv;
    let baseColor = linearSample(baseColorTexture, baseColorSampler, uv).rgb;
    let metalRough = textureSample(metallicRoughnessTexture, metallicRoughnessSampler, uv);
    let metallic = metalRough.b;
    let roughness = clamp(metalRough.g, 0.04, 1.0);

    let normalMap = textureSample(normalTexture, normalSampler, uv).rgb;
    let normal = normalize(normalMap * 2.0 - 1.0);
    let world_normal = normalize(in.world_normal + normal);

    let ao = textureSample(occlusionTexture, occlusionSampler, uv).r;
    let emissive = textureSample(emissiveTexture, emissiveSampler, uv).rgb;

    let lightDir = normalize(vec3<f32>(2.0, 4.0, 3.0)); // Example light direction
    let viewDir = normalize(vec3<f32>(0.0, 0.0, 1.0)); // Example view direction

    let color = brdf(baseColor, metallic, roughness, lightDir, viewDir, world_normal) * ao + emissive;
    color = pow(color, vec3<f32>(1.0 / 2.2)); // Gamma correction

    return vec4<f32>(color, 1.0); // Assuming alpha is always 1.0
}
