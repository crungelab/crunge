from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""

def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    logger.debug("Creating pipeline")

    logger.debug("Creating shader module")
    shader_module = utils.create_shader_module(device, shader_code)
    logger.debug(shader_module)

    logger.debug("Creating colorTargetStates")

    colorTargetStates = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

    logger.debug(colorTargetStates)
    logger.debug(colorTargetStates[0].format)
    logger.debug(colorTargetStates[0].format.value)

    logger.debug("Creating fragmentState")
    fragmentState = wgpu.FragmentState(
        module=shader_module,
        entry_point="fs_main",
        targets=colorTargetStates,
    )

    logger.debug(fragmentState)
    logger.debug(fragmentState.entry_point)

    logger.debug("Creating depthStencilState")
    depthStencilState = wgpu.DepthStencilState(
        format=wgpu.TextureFormat.DEPTH32_FLOAT,
        depth_write_enabled=False
    )
    logger.debug(depthStencilState)

    logger.debug("Creating primitive")
    primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST)
    logger.debug(primitive)

    logger.debug("Creating vertex_state")
    vertex_state = wgpu.VertexState(
        module=shader_module,
        entry_point="vs_main",
    )
    logger.debug(vertex_state)

    logger.debug("Creating multisample")
    multisample = wgpu.MultisampleState(
        count=1,
        mask=0xFFFFFFFF,
        alpha_to_coverage_enabled=False,
    )

    logger.debug(multisample.count)
    logger.debug(hex(multisample.mask))
    logger.debug(multisample.alpha_to_coverage_enabled)

    logger.debug("Creating render pipeline descriptor")
    descriptor = wgpu.RenderPipelineDescriptor(
        label="Main Render Pipeline",
        vertex=vertex_state,
        primitive=primitive,
        #layout=device.create_pipeline_layout(),
        #layout=None,
        depth_stencil=depthStencilState,
        multisample=multisample,
        fragment=fragmentState,
    )
    logger.debug(descriptor)
    logger.debug(descriptor.fragment.targets[0].format)

    logger.debug("Creating render pipeline")
    pipeline = device.create_render_pipeline(descriptor)
    logger.debug(pipeline)


if __name__ == "__main__":
    main()