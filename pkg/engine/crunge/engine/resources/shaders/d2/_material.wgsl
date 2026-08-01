struct Material {
    color : vec4<f32>,
    spriteRect : vec4<f32>, // x, y, width, height
    textureSize : vec2<f32>,
    flipFlags : u32, // Bitwise combination of FLIP_H, FLIP_V, FLIP_D
}

//@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.MATERIAL_UNIFORM}}) var<uniform> material : Material;
@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.SAMPLER}}) var mySampler: sampler;
//@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.TEXTURE}}) var myTexture : texture_2d<f32>;
@group({{BindGroupIndex.MATERIAL}}) @binding({{MaterialBindIndex.TEXTURE}}) var myTexture : texture_2d_array<f32>;
