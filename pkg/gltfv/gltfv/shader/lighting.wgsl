// Assuming 'fragPos' is the position of the fragment in world space
let lightDir = normalize(light.position - fragPos);
let viewDir = normalize(cameraPos - fragPos); // cameraPos should also be passed as a uniform
let lightColor = light.color * light.intensity;

// Apply the BRDF to compute the reflection at this point
let reflection = brdf(albedo.rgb, metallic, roughness, lightDir, viewDir, normal);

// Calculate the final color, considering the light color and ambient occlusion
let rgb = reflection * lightColor * ao + emissive;

// Apply gamma correction to convert the linear RGB color to sRGB
let finalColor = linearToSRGB(rgb);
return vec4<f32>(finalColor, albedo.a);
