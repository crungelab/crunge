from loguru import logger

import numpy as np

from crunge import wgpu
from crunge.wgpu import utils
from crunge import gltf

from ..constants import TEXTURE_BINDING_START
from . import Builder
from .builder_context import BuilderContext
from ..debug import (
    debug_accessor,
    debug_material,
)

from crunge.engine.d3.mesh import Mesh
from crunge.engine.d3.primitive import Primitive
from crunge.engine.resource.cube_texture import CubeTexture

from .vertex_table import VertexTable
from .vertex_column import PosColumn, NormalColumn, UvColumn, RgbaColumn, TangentColumn

from .material_builder import MaterialBuilder
from crunge.engine.resource.material import Material

from ..normals import compute_normals
from ..tangents import compute_tangents


class PrimitiveBuilder(Builder):
    def __init__(
        self, context: BuilderContext, mesh: Mesh, tf_primitive: gltf.Primitive
    ) -> None:
        super().__init__(context)
        self.mesh = mesh
        self.tf_primitive = tf_primitive
        self.primitive = Primitive()
        self.material = Material()

        self.vertex_table = VertexTable()

    def build(self):
        self.build_indices()
        self.build_material()
        self.build_attributes()
        self.build_pipeline()
        self.build_bindgroup()

        vertex_data = self.vertex_table.data

        self.primitive.vertex_data = vertex_data
        self.primitive.vertex_buffer = self.gfx.create_buffer_from_ndarray(
            "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

        return self.primitive

    def build_attributes(self):
        tf_primitive = self.tf_primitive
        attributes: dict = tf_primitive.attributes.copy()
        pos = attributes.get("POSITION", None)
        if pos is not None:
            self.build_attribute(("POSITION", pos))
            del attributes["POSITION"]
        for attribute in attributes.items():
            self.build_attribute(attribute)

        if not self.vertex_table.has("normal"):
            normals = compute_normals(
                self.primitive.index_data, self.vertex_table.get("pos").data
            )
            self.vertex_table.add_column(NormalColumn("normal", normals))

        if self.vertex_table.has("uv"):
            if not self.vertex_table.has("tangent"):
                tangents = compute_tangents(
                    self.primitive.index_data,
                    self.vertex_table.get("pos").data,
                    self.vertex_table.get("uv").data,
                    self.vertex_table.get("normal").data,
                )
                self.vertex_table.add_column(TangentColumn("tangent", tangents))

    def build_attribute(self, attribute: tuple):
        name, value = attribute
        logger.debug(f"primitive.attributes[{name}]: {value}")
        accessor = self.tf_model.accessors[value]
        debug_accessor(accessor)

        buffer_view = self.tf_model.buffer_views[accessor.buffer_view]
        buffer = self.tf_model.buffers[buffer_view.buffer]
        logger.debug(f"buffer_view: {buffer_view}")
        logger.debug(f"buffer: {buffer}")

        component_type = accessor.component_type
        logger.debug(f"component_type: {component_type}")
        count = accessor.count
        logger.debug(f"count: {count}")
        type = accessor.type
        logger.debug(f"type: {type}")
        data = buffer.get_array(
            buffer_view.byte_offset + accessor.byte_offset, count, type, component_type
        )

        if name == "POSITION":
            self.vertex_table.add_column(PosColumn("pos", data))
        elif name == "NORMAL":
            self.vertex_table.add_column(NormalColumn("normal", data))
        elif name == "TANGENT":
            self.vertex_table.add_column(TangentColumn("tangent", data))
        elif name == "TEXCOORD_0":
            self.vertex_table.add_column(UvColumn("uv", data))
        elif name == "COLOR_0":
            self.vertex_table.add_column(RgbaColumn("color", data))
        elif name == "JOINTS_0":
            return
        elif name == "WEIGHTS_0":
            return
        else:
            # logger.debug(f"Unknown attribute: {name}")
            raise Exception(f"Unknown attribute: {name}")

        # logger.debug(f"data: {data}")

    def build_indices(self):
        tf_primitive = self.tf_primitive
        logger.debug(f"primitive.indices: {tf_primitive.indices}")
        accessor = self.tf_model.accessors[tf_primitive.indices]
        debug_accessor(accessor)

        buffer_view = self.tf_model.buffer_views[accessor.buffer_view]
        buffer = self.tf_model.buffers[buffer_view.buffer]
        logger.debug(f"buffer_view: {buffer_view}")
        logger.debug(f"buffer: {buffer}")

        type = accessor.type
        logger.debug(f"type: {type}")

        component_type = accessor.component_type
        logger.debug(f"component_type: {component_type}")
        if component_type == gltf.ComponentType.UNSIGNED_SHORT:
            self.primitive.index_format = wgpu.IndexFormat.UINT16
        elif component_type == gltf.ComponentType.UNSIGNED_INT:
            self.primitive.index_format = wgpu.IndexFormat.UINT32

        count = accessor.count
        logger.debug(f"count: {count}")
        indices = buffer.get_array(
            buffer_view.byte_offset + accessor.byte_offset, count, type, component_type
        )

        # logger.debug(f"indices: {indices}")

        self.primitive.index_data = indices
        self.primitive.index_buffer = self.gfx.create_buffer_from_ndarray(
            "INDEX", indices, wgpu.BufferUsage.INDEX
        )

    def build_vertex_attributes(self):
        logger.debug("Creating vertex attributes")
        vert_attributes = wgpu.VertexAttributes()
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

    def build_material(self):
        if self.tf_primitive.material < 0:
            return
        tf_primitive = self.tf_primitive
        logger.debug(f"primitive.material: {tf_primitive.material}")
        tf_material = self.tf_model.materials[tf_primitive.material]
        debug_material(tf_material)
        self.material = MaterialBuilder(self.context, tf_material).build()
        # exit()

    def build_pipeline(self):
        logger.debug("Creating pipeline")

        vs_module: wgpu.ShaderModule = self.context.vertex_shader_builder_class(
            self.context, self.vertex_table
        ).build()
        fs_module: wgpu.ShaderModule = self.context.fragment_shader_builder_class(
            self.context, self.vertex_table, self.material
        ).build()

        vertAttributes = self.build_vertex_attributes()

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=self.vertex_table.vertex_size,
                attribute_count=self.vertex_table.count,
                attributes=vertAttributes,
            )
        ]

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayouts,
        )

        blend_state: wgpu.BlendState = None

        if self.material.alpha_mode == "BLEND":
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

        fragmentState = wgpu.FragmentState(
            module=fs_module,
            entry_point="fs_main",
            target_count=1,
            targets=color_targets,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=True,
            depth_compare=wgpu.CompareFunction.LESS,
        )

        primitive = wgpu.PrimitiveState(cull_mode=wgpu.CullMode.BACK)

        bgl_entries = [
            # Camera
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            # Ambient Light
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            # Light
            wgpu.BindGroupLayoutEntry(
                binding=2,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        for i, texture in enumerate(self.material.textures):
            view_dimension = wgpu.TextureViewDimension.E2D
            if isinstance(texture, CubeTexture):
                view_dimension = wgpu.TextureViewDimension.CUBE

            bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + TEXTURE_BINDING_START,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    sampler=wgpu.SamplerBindingLayout(
                        type=wgpu.SamplerBindingType.FILTERING
                    ),
                )
            )
            bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + TEXTURE_BINDING_START + 1,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    texture=wgpu.TextureBindingLayout(
                        sample_type=wgpu.TextureSampleType.FLOAT,
                        #view_dimension=wgpu.TextureViewDimension.E2D,
                        view_dimension=view_dimension,
                    ),
                )
            )

        bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(bgl_entries), entries=bgl_entries
        )
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=[bgl]
        )

        multisample = wgpu.MultisampleState(
            count=1,
            #count=4,
        )

        rp_descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            multisample=multisample,
            fragment=fragmentState,
        )
        logger.debug("Creating render pipeline")
        self.primitive.pipeline = self.device.create_render_pipeline(rp_descriptor)

    def build_bindgroup(self):
        logger.debug("Creating bind group")
        bg_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.mesh.camera_uniform_buffer,
                size=self.mesh.camera_uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=1,
                buffer=self.scene.ambient_light.uniform_buffer,
                size=self.scene.ambient_light.uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=2,
                #buffer=self.mesh.light_uniform_buffer,
                buffer=self.scene.lighting.lights[0].uniform_buffer,
                #size=self.mesh.light_uniform_buffer_size,
                size=self.scene.lighting.lights[0].uniform_buffer_size,
            ),
        ]

        for i, texture in enumerate(self.material.textures):
            bg_entries.append(
                wgpu.BindGroupEntry(
                    binding=i * 2 + TEXTURE_BINDING_START, sampler=texture.sampler
                )
            )
            bg_entries.append(
                wgpu.BindGroupEntry(
                    binding=i * 2 + TEXTURE_BINDING_START + 1, texture_view=texture.view
                )
            )

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Uniform bind group",
            layout=self.primitive.pipeline.get_bind_group_layout(0),
            entry_count=len(bg_entries),
            entries=bg_entries,
        )

        self.primitive.bind_group = self.device.create_bind_group(bindGroupDesc)