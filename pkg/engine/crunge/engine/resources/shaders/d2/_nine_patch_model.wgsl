// Same prefix as Model in _model.wgsl, so the sprite update code can fill the
// first 48 bytes unchanged. Keep the two in sync.
struct NinePatchModel {
    color : vec4<f32>,
    spriteRect : vec4<f32>, // x, y, width, height in texels
    textureSize : vec2<f32>,
    flipFlags : u32, // Bitmask for flip flags
    texture_layer : i32, // Layer for texture array
    insets : vec4<f32>, // normalized left, top, right, bottom
    borderScale : f32, // texels -> local units: border thickness and the size of one repeat
    fillFlags : u32, // FILL_TILE_X | FILL_TILE_Y; unset axes stretch
    _pad : vec2<f32>,
}

@group({{BindGroupIndex.MODEL}}) @binding({{ModelBindIndex.MODEL_UNIFORM}}) var<uniform> model : NinePatchModel;
