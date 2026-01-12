from loguru import logger

from crunge import wgpu

from ....d3.material_3d import Material3D
from ....d3.primitive_3d import Primitive3DProgram

from ..constants import SAMPLE_COUNT

from . import GltfBuilder
from .builder_context import BuilderContext
from .vertex_table import VertexTable


class ProgramBuilder(GltfBuilder):
    def __init__(
        self,
        context: BuilderContext,
        vertex_table: VertexTable,
        material: Material3D,
        write_depth: bool = True,
        write_color: bool = True,
    ) -> None:
        super().__init__(context)
        self.vertex_table = vertex_table
        self.material = material
        self.write_depth = write_depth
        self.write_color = write_color
        self.program = Primitive3DProgram()

    def build(self) -> Primitive3DProgram:
        logger.debug("Creating Program")

        vs_module: wgpu.ShaderModule = self.context.vertex_shader_builder_class(
            self.context, self.vertex_table
        ).build()
        fs_module: wgpu.ShaderModule = self.context.fragment_shader_builder_class(
            self.context, self.vertex_table, self.material
        ).build()

        vertex_attributes = self.build_vertex_attributes()

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=self.vertex_table.vertex_size,
                attributes=vertex_attributes,
            )
        ]

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="vs_main",
            buffers=vertBufferLayouts,
        )

        blend_state: wgpu.BlendState = None

        if self.material.alpha_mode == "BLEND" and self.write_color:
            logger.debug("Using blend state for alpha mode 'BLEND'")
            blend_state = wgpu.BlendState(
                color=wgpu.BlendComponent(
                    operation=wgpu.BlendOperation.ADD,
                    src_factor=wgpu.BlendFactor.SRC_ALPHA,
                    dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
                ),
                alpha=wgpu.BlendComponent(
                    operation=wgpu.BlendOperation.ADD,
                    src_factor=wgpu.BlendFactor.ONE,
                    dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
                ),
            )

        #write_mask = wgpu.ColorWriteMask.ALL if self.write_color else wgpu.ColorWriteMask.NONE
        write_mask = wgpu.ColorWriteMask.ALL
        logger.debug(f"Color write mask: {write_mask}")

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
                write_mask=write_mask,
            )
        ]

        fragment_state = wgpu.FragmentState(
            module=fs_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        depth_write_enabled = self.write_depth
        logger.debug(f"Depth write enabled: {depth_write_enabled}")

        depth_compare = wgpu.CompareFunction.LESS_EQUAL if depth_write_enabled else wgpu.CompareFunction.NEVER

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=depth_write_enabled,
            depth_compare=depth_compare,
        )

        cull_mode = wgpu.CullMode.NONE if self.material.double_sided else wgpu.CullMode.BACK
        logger.debug(f"Cull mode: {cull_mode}")
    
        primitive = wgpu.PrimitiveState(cull_mode=cull_mode)

        bind_group_layouts = [
            self.program.camera_bind_group_layout,
            self.program.light_bind_group_layout,
            self.material.bind_group_layout,
            self.program.model_bind_group_layout,
        ]

        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=bind_group_layouts)

        multisample = wgpu.MultisampleState(
            count=SAMPLE_COUNT,
        )

        rp_descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depth_stencil_state,
            multisample=multisample,
            fragment=fragment_state,
        )
        logger.debug("Creating render pipeline")
        self.program.pipeline = self.device.create_render_pipeline(rp_descriptor)
        return self.program

    def build_vertex_attributes(self):
        logger.debug("Creating vertex attributes")
        vert_attributes = []
        offset = 0
        for location, column in enumerate(self.vertex_table.columns):
            vert_attributes.append(
                wgpu.VertexAttribute(
                    format=column.format,
                    offset=offset,
                    shader_location=location,
                )
            )
            offset += column.struct_size
        return vert_attributes
