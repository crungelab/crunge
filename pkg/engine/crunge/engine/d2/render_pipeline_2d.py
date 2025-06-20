from typing import List

from loguru import logger

from crunge import wgpu

from ..render_pipeline import RenderPipeline

from ..bindings import (
    ViewportBindGroupLayout,
)

from .bindings import (
    CameraBindGroupLayout,
    SpriteBindGroupLayout,
    ModelBindGroupLayout,
)


class RenderPipeline2D(RenderPipeline):
    def __init__(self, vertex_shader_module=None, fragment_shader_module=None):
        super().__init__()
        self.vertex_shader_module = vertex_shader_module
        self.fragment_shader_module = fragment_shader_module

    @property
    def viewport_bind_group_layout(self):
        return ViewportBindGroupLayout()

    @property
    def camera_bind_group_layout(self):
        return CameraBindGroupLayout()

    @property
    def material_bind_group_layout(self):
        return SpriteBindGroupLayout()

    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout()

    @property
    def bind_group_layouts(self) -> list[wgpu.BindGroupLayout]:
        bind_group_layouts = [
            self.viewport_bind_group_layout.get(),
            self.camera_bind_group_layout.get(),
            self.material_bind_group_layout.get(),
            self.model_bind_group_layout.get(),
        ]

        return bind_group_layouts
    
    def create_vertex_state(self):
        return wgpu.VertexState(
            module=self.vertex_shader_module,
            entry_point="vs_main",
        )
    
    def create_fragment_state(self):
        # Had to hold on to blend_state because of garbage collection issues
        # TODO: Why isn't color_targets having the same issue?
        self.blend_state = wgpu.BlendState(
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
                blend=self.blend_state,
                write_mask=wgpu.ColorWriteMask.ALL,
            )
        ]

        fragment_state = wgpu.FragmentState(
            module=self.fragment_shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )
        return fragment_state

    def create_primitive_state(self):
        return wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

    def _create(self):
        '''
        vertex_state = wgpu.VertexState(
            module=self.vertex_shader_module,
            entry_point="vs_main",
        )
        '''
        vertex_state = self.create_vertex_state()
        '''
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
            module=self.fragment_shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )
        '''
        fragment_state = self.create_fragment_state()

        #primitive_state = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)
        primitive_state = self.create_primitive_state()

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            # depth_write_enabled=True,
            depth_write_enabled=False,
            # depth_compare = wgpu.CompareFunction.LESS,
        )

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.bind_group_layouts
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Sprite Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive_state,
            fragment=fragment_state,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)
