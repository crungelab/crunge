const PI = 3.141592741;

fn FresnelSchlick(cosTheta : f32, F0 : vec3<f32>) -> vec3<f32> {
  return (F0 + ((vec3(1.0) - F0) * pow((1.0 - cosTheta), 5.0)));
}

fn DistributionGGX(N : vec3<f32>, H : vec3<f32>, roughness : f32) -> f32 {
  let a = (roughness * roughness);
  let a2 = (a * a);
  let NdotH = max(dot(N, H), 0.0);
  let NdotH2 = (NdotH * NdotH);
  let num = a2;
  let denom = ((NdotH2 * (a2 - 1.0)) + 1.0);
  return (num / ((PI * denom) * denom));
}

fn GeometrySchlickGGX(NdotV : f32, roughness : f32) -> f32 {
  let r = (roughness + 1.0);
  let k = ((r * r) / 8.0);
  let num = NdotV;
  let denom = ((NdotV * (1.0 - k)) + k);
  return (num / denom);
}

fn GeometrySmith(N : vec3<f32>, V : vec3<f32>, L : vec3<f32>, roughness : f32) -> f32 {
  let NdotV = max(dot(N, V), 0.0);
  let NdotL = max(dot(N, L), 0.0);
  let ggx2 = GeometrySchlickGGX(NdotV, roughness);
  let ggx1 = GeometrySchlickGGX(NdotL, roughness);
  return (ggx1 * ggx2);
}

fn lightAttenuation(light : Light) -> f32 {
  if ((light.kind == LightKind_Directional)) {
    return 1.0;
  }
  let distance = length(light.v);
  if ((light.range <= 0.0)) {
    return (1.0 / pow(distance, 2.0));
  }
  return (clamp((1.0 - pow((distance / light.range), 4.0)), 0.0, 1.0) / pow(distance, 2.0));
}

fn lightRadiance(light : Light, surface : Surface) -> vec3<f32> {
  let L = normalize(light.v);
  let H = normalize((surface.v + L));
  let NDF = DistributionGGX(surface.normal, H, surface.roughness);
  let G = GeometrySmith(surface.normal, surface.v, L, surface.roughness);
  let F = FresnelSchlick(max(dot(H, surface.v), 0.0), surface.f0);
  let kD = ((vec3(1.0) - F) * (1.0 - surface.metallic));
  let NdotL = max(dot(surface.normal, L), 0.0);
  let numerator = ((NDF * G) * F);
  //let denominator = max(((4.0 * max(dot(surface.normal, surface.v), 0.0)) * NdotL), 0.001);
  let denominator = max( (max(dot(surface.normal, surface.v), 0.0) * NdotL), 0.001);
  let specular = (numerator / vec3(denominator));
  let radiance = ((light.color * light.energy) * lightAttenuation(light));
  return (((((kD * surface.albedo) / vec3(PI)) + specular) * radiance) * NdotL);
}
