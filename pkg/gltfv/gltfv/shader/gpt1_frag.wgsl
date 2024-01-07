// ... (Uniforms and VertexInput/Output structures are the same as in the vertex shader)

@group(0) @binding(1) var baseColorSampler: sampler;
@group(0) @binding(2) var baseColorTexture : texture_2d<f32>;
// ... (Other texture and sampler bindings)

// Utility function for gamma correction
fn sRGBToLinear(color: vec3<f32>) -> vec3<f32> {
    return pow(color, vec3<f32>(2.2));
}

fn linearToSRGB(color: vec3<f32>) -> vec3<f32> {
    return pow(color, vec3<f32>(1.0 / 2.2));
}

// ... (Other utility functions like blinnPhong and brdf)

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    let uv = in.uv;

    var albedo = textureSample(baseColorTexture, baseColorSampler, uv).rgb;
    albedo = sRGBToLinear(albedo); // Convert to linear space

    // ... (Sample other textures and convert if necessary)

    var normal = normalize(in.normal); // Use the passed normal
    // If using normal maps, replace the above with the appropriate transformation

    // Calculate dynamic values based on the camera and scene
    let cameraPos = vec3<f32>(0.0, 0.0, 1.0); // This should be passed as a uniform
    let fragPos = vec3<f32>(in.vertex_pos.xyz); // Extract position
    let viewDir = normalize(cameraPos - fragPos);

    // ... (Perform lighting calculations using brdf and other models)

    // Apply ambient occlusion and emissive as needed
    // ...

    // Convert the final color back to sRGB space before outputting
    let finalColor = linearToSRGB(rgb);
    return vec4<f32>(finalColor, 1.0); // Use the alpha from your texture if needed
}
