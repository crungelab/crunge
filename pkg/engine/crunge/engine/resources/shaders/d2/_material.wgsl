struct Material {
    color : vec4<f32>,
    spriteRect : vec4<f32>, // x, y, width, height
    textureSize : vec2<f32>,
    flipH : u32, // 1 = true, 0 = false
    flipV : u32, // 1 = true, 0 = false
}

@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.SAMPLER}}) var mySampler: sampler;
@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.TEXTURE}}) var myTexture : texture_2d<f32>;
@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.MATERIAL_UNIFORM}}) var<uniform> material : Material;
