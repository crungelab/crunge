from loguru import logger

from crunge import wgpu

from .program import Program
from .loader.shader_loader import ShaderLoader


class Blitter(Program):
    def __init__(self, surface_texture, color_texture):
        super().__init__()
        self.surface_texture = surface_texture
        self.color_texture = color_texture

        # Create the shader module, pipeline layout, and render pipeline
        self._create_pipeline()

    def _create_pipeline(self):
        # Create shader module
        shader_module = ShaderLoader(self.template_env, {}).load("blitter.wgsl")

        # Create bind group layout
        bg_layout = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(
                entries=[
                    wgpu.BindGroupLayoutEntry(
                        binding=0,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        texture=wgpu.TextureBindingLayout(
                            sample_type=wgpu.TextureSampleType.FLOAT
                        ),
                    ),
                    wgpu.BindGroupLayoutEntry(
                        binding=1,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        sampler=wgpu.SamplerBindingLayout(
                            type=wgpu.SamplerBindingType.FILTERING
                        ),
                    ),
                ]
            )
        )

        # Create pipeline layout
        pipeline_layout = self.device.create_pipeline_layout(
            wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bg_layout])
        )

        # Create render pipeline
        self.pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                layout=pipeline_layout,
                vertex=wgpu.VertexState(
                    module=shader_module,
                    entry_point="vs_main",
                ),
                fragment=wgpu.FragmentState(
                    module=shader_module,
                    entry_point="fs_main",
                    targets=[
                        wgpu.ColorTargetState(
                            format=wgpu.TextureFormat.BGRA8_UNORM,  # Match your surface texture format
                        )
                    ],
                ),
                primitive=wgpu.PrimitiveState(
                    topology=wgpu.PrimitiveTopology.TRIANGLE_LIST,
                    strip_index_format=wgpu.IndexFormat.UNDEFINED,
                    front_face=wgpu.FrontFace.CW,
                    cull_mode=wgpu.CullMode.NONE,
                ),
            )
        )

        # Create bind group
        src_view = self.color_texture.create_view()
        src_sampler = self.device.create_sampler(
            wgpu.SamplerDescriptor(
                mag_filter=wgpu.FilterMode.LINEAR, min_filter=wgpu.FilterMode.LINEAR
            )
        )
        self.bind_group = self.device.create_bind_group(
            wgpu.BindGroupDescriptor(
                layout=bg_layout,
                entries=[
                    wgpu.BindGroupEntry(binding=0, texture_view=src_view),
                    wgpu.BindGroupEntry(binding=1, sampler=src_sampler),
                ],
            )
        )

    def blit(self):
        logger.debug("Blitting to surface texture")
        encoder = self.device.create_command_encoder()

        render_pass = encoder.begin_render_pass(
            wgpu.RenderPassDescriptor(
                color_attachments=[
                    wgpu.RenderPassColorAttachment(
                        view=self.surface_texture.create_view(),
                        clear_value=wgpu.Color(0, 0, 0, 1),
                        store_op=wgpu.StoreOp.STORE,
                    )
                ],
            )
        )
        render_pass.set_pipeline(self.pipeline)
        render_pass.set_bind_group(0, self.bind_group)
        render_pass.draw(3, 1, 0, 0)  # 3 verts, 1 instance
        render_pass.end()
