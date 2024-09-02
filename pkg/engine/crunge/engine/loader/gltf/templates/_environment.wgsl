fn directionToEquirectangularUV(direction: vec3<f32>) -> vec2<f32> {
    // Calculate spherical coordinates
    let theta = atan2(direction.z, direction.x); // Longitude [-π, π]
    let phi = asin(direction.y);                  // Latitude [-π/2, π/2]

    // Map spherical coordinates to texture coordinates
    let u = (theta / (2.0 * pi)) + 0.5;
    let v = (phi / pi) + 0.5;
    return vec2<f32>(u, v);
}
