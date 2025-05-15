from crunge import wgpu

shader_code = """
@vertex
fn main_v(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn main_f() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""

def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    #wgsl_desc = wgpu.ShaderModuleWGSLDescriptor(source=shader_code)
    wgsl_desc = wgpu.ShaderSourceWGSL(code=shader_code)
    print(wgsl_desc)
    descriptor = wgpu.ShaderModuleDescriptor()
    descriptor.next_in_chain = wgsl_desc
    shader_module = device.create_shader_module(descriptor)
    print(shader_module)

if __name__ == "__main__":
    main()