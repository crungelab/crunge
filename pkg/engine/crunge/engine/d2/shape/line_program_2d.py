from ctypes import sizeof, c_float

from loguru import logger

from crunge.core import klass
from crunge import wgpu

from crunge.engine.d2.program_2d import Program2D

from ...resource.bind_group.bind_group_layout import BindGroupLayout
from ...loader.shader_loader import ShaderLoader


@klass.singleton
class MaterialBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries, label="LineMaterialBindGroupLayout")


@klass.singleton
class LineProgram2D(Program2D):
    pipeline: wgpu.RenderPipeline = None

    def __init__(self):
        super().__init__()
        self.create_render_pipeline()

    @property
    def material_bind_group_layout(self):
        return MaterialBindGroupLayout().get()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "line.wgsl"
        )

        vertex_attributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
        ]

        vertex_buffer_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=2 * sizeof(c_float),
                attributes=vertex_attributes,
            )
        ]

        blend_state = wgpu.BlendState(
            alpha=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.ONE,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
            color=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.SRC_ALPHA,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
        )

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
                write_mask=wgpu.ColorWriteMask.ALL,
            )
        ]

        fragment_state = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffers=vertex_buffer_layouts,
        )

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            # depth_write_enabled=True,
            depth_write_enabled=False,
            # depth_compare = wgpu.CompareFunction.LESS,
        )

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.bind_group_layouts
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.LINE_LIST)

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            primitive=primitive,
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragment_state,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)
