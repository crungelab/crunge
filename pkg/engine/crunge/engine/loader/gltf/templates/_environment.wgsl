// Convert a reflection vector to equirectangular coordinates
fn reflectionToEquirectangularUV(viewDir: vec3<f32>, normal: vec3<f32>) -> vec2<f32> {
    //let reflection = normalize(-reflect(viewDir, normal));

    // Calculate spherical coordinates
    //let theta = atan2(reflection.z, reflection.x); // Longitude [-π, π]
    //let phi = asin(reflection.y);                  // Latitude [-π/2, π/2]
    // Map spherical coordinates to texture coordinates
    //let u = (theta / (2.0 * pi)) + 0.5;
    //let v = (phi / pi) + 0.5;

    let reflection = normalize(reflect(viewDir, normal));
    let phi = atan2(reflection.z, reflection.x);
    let theta = acos(reflection.y);
    let u = (phi / (2.0 * 3.141592653589793)) + 0.5;
    let v = theta / 3.141592653589793;
    
    return vec2<f32>(u, v);
}
