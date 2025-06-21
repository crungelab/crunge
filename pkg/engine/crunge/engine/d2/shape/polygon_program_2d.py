from ctypes import sizeof, c_float

from loguru import logger

from crunge.core import klass
from crunge import wgpu

from crunge.engine.d2.program_2d import Program2D

from ...loader.shader_loader import ShaderLoader

from ..bindings_2d import ShapeBindGroupLayout
from ..render_pipeline_2d import RenderPipeline2D


class PolygonRenderPipeline2D(RenderPipeline2D):
    @property
    def material_bind_group_layout(self):
        return ShapeBindGroupLayout()

    def create_vertex_state(self):
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

        vertex_state = wgpu.VertexState(
            module=self.vertex_shader_module,
            entry_point="vs_main",
            buffers=vertex_buffer_layouts,
        )
        return vertex_state

    def create_primitive_state(self):
        return wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.LINE_STRIP)

@klass.singleton
class PolygonProgram2D(Program2D):
    def __init__(self):
        super().__init__()
        self.render_pipeline: PolygonRenderPipeline2D = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "polygon.wgsl"
        )

        self.render_pipeline = PolygonRenderPipeline2D(
            vertex_shader_module=shader_module, fragment_shader_module=shader_module
        ).create()
