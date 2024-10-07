from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .camera_2d import Camera2D

from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)
from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu
from crunge import engine

from .uniforms_2d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    LightUniform,
    Mat4,
)


class Renderer2D(engine.Renderer):
    camera_uniform_buffer: wgpu.Buffer = None
    camera_uniform_buffer_size: int = 0

    def __init__(self, camera: "Camera2D") -> None:
        super().__init__()
        self.camera = camera
        self.encoder: wgpu.CommandEncoder = None
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.create_buffers()
        self.create_bind_groups()

    def create_buffers(self):
        # Uniform Buffers
        self.camera_uniform_buffer_size = sizeof(CameraUniform)
        self.camera_uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.camera_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(camera_bgl_entries), entries=camera_bgl_entries
        )
        camera_bgl = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {camera_bgl}")

        camera_bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.camera_uniform_buffer,
                size=self.camera_uniform_buffer_size,
            ),
        ]

        camera_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Camera bind group",
            layout=camera_bgl,
            entry_count=len(camera_bindgroup_entries),
            entries=camera_bindgroup_entries,
        )

        self.camera_bind_group = self.device.create_bind_group(camera_bind_group_desc)

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def begin(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.camera.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.camera.view_matrix)
        camera_uniform.position = cast_vec3(
            glm.vec3(self.camera.position.x, self.camera.position.y, 0)
        )

        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                #view=self.texture_view,
                view=self.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            #view=self.depth_stencil_view,
            view=self.viewport.depth_stencil_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        self.encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        self.pass_enc: wgpu.RenderPassEncoder = self.encoder.begin_render_pass(
            renderpass
        )
        self.pass_enc.set_bind_group(0, self.camera_bind_group)

    def end(self):
        self.pass_enc.end()
        commands = self.encoder.finish()
        self.device.queue.submit(1, commands)
