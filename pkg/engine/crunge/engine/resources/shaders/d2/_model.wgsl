struct Model {
    color : vec4<f32>,
    spriteRect : vec4<f32>, // x, y, width, height
    textureSize : vec2<f32>,
    flipH : u32, // 1 = true, 0 = false
    flipV : u32, // 1 = true, 0 = false
    layer : i32, // Layer for texture array
}

@group({{BindGroupIndex.MODEL}}) @binding({{ModelBindIndex.MODEL_UNIFORM}}) var<uniform> model : Model;
