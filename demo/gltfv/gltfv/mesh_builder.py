from loguru import logger

import numpy as np

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import gltf

from .constants import RESERVED_BINDINGS, TEXTURE_BINDING_START
from .node_builder import NodeBuilder
from .node import Node
from .debug import (
    debug_node,
    debug_mesh,
    debug_primitive,
    debug_accessor,
    debug_material,
)

from .mesh import Mesh

from .vertex_table import VertexTable
from .vertex_column import PosColumn, NormalColumn, UvColumn, RgbaColumn, TangentColumn

from .material_builder import MaterialBuilder
from .material import Material

# from .shader import VertexShaderBuilder, FragmentShaderBuilder
from .shader_og import VertexShaderBuilder, FragmentShaderBuilder

# from .shader2 import VertexShaderBuilder, FragmentShaderBuilder

from .normals import compute_normals
from .tangents import compute_tangents


class MeshBuilder(NodeBuilder):
    def __init__(self, tf_model: gltf.Model, tf_node: gltf.Node) -> None:
        super().__init__(tf_model, tf_node)
        self.tf_mesh = tf_model.meshes[self.tf_node.mesh]
        self.mesh: Mesh = None
        self.material = Material()

        self.vertex_table = VertexTable()

    def create_node(self):
        self.node = self.mesh = Mesh()

    def build_node(self):
        super().build_node()
        debug_mesh(self.tf_mesh)
        self.build_primitives()
        self.build_pipeline()
        self.build_bindgroup()

    def build_primitives(self):
        for primitive in self.tf_mesh.primitives:
            self.build_primitive(primitive)
        # Vertex Data
        vertex_data = self.vertex_table.data

        self.mesh.vertex_data = vertex_data
        self.mesh.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

    def build_primitive(self, primitive: gltf.Primitive):
        debug_primitive(primitive)

        if primitive.indices >= 0 and primitive.indices < len(self.tf_model.accessors):
            self.build_indices(primitive)
        if primitive.material >= 0 and primitive.material < len(
            self.tf_model.materials
        ):
            self.build_material(primitive)

        self.build_attributes(primitive)

    def build_attributes(self, primitive: gltf.Primitive):
        attributes: dict = primitive.attributes.copy()
        pos = attributes.get("POSITION", None)
        if pos:
            self.build_attribute(("POSITION", pos))
            del attributes["POSITION"]
        for attribute in attributes.items():
            self.build_attribute(attribute)

        if not self.vertex_table.has("normal"):
            normals = compute_normals(
                self.mesh.index_data, self.vertex_table.get("pos").data
            )
            self.vertex_table.add_column(NormalColumn("normal", normals))

        if self.vertex_table.has("uv"):
            if not self.vertex_table.has("tangent"):
                tangents = compute_tangents(
                    self.mesh.index_data,
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

    def build_indices(self, primitive: gltf.Primitive):
        logger.debug(f"primitive.indices: {primitive.indices}")
        accessor = self.tf_model.accessors[primitive.indices]
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
            self.mesh.index_format = wgpu.IndexFormat.UINT16
        elif component_type == gltf.ComponentType.UNSIGNED_INT:
            self.mesh.index_format = wgpu.IndexFormat.UINT32

        count = accessor.count
        logger.debug(f"count: {count}")
        indices = buffer.get_array(
            buffer_view.byte_offset + accessor.byte_offset, count, type, component_type
        )

        # logger.debug(f"indices: {indices}")

        self.mesh.index_data = indices
        self.mesh.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", indices, wgpu.BufferUsage.INDEX
        )
        # exit()

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

    def build_material(self, primitive: gltf.Primitive):
        logger.debug(f"primitive.material: {primitive.material}")
        material = self.tf_model.materials[primitive.material]
        debug_material(material)
        self.material = MaterialBuilder(self.tf_model, material).build()

    def build_pipeline(self):
        logger.debug("Creating pipeline")
        vs_module: wgpu.ShaderModule = VertexShaderBuilder(self.vertex_table).build()
        fs_module: wgpu.ShaderModule = FragmentShaderBuilder(
            self.vertex_table, self.material
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
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        for i, texture in enumerate(self.material.textures):
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
                        view_dimension=wgpu.TextureViewDimension.E2D,
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

        rp_descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )

        self.mesh.pipeline = self.device.create_render_pipeline(rp_descriptor)

    def build_bindgroup(self):
        bg_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.mesh.camera_uniform_buffer,
                    size=self.mesh.camera_uniform_buffer_size,
                ),
                wgpu.BindGroupEntry(
                    binding=1,
                    buffer=self.mesh.light_uniform_buffer,
                    size=self.mesh.light_uniform_buffer_size,
                ),
            ]
        )

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
            layout=self.mesh.pipeline.get_bind_group_layout(0),
            entry_count=len(bg_entries),
            entries=bg_entries,
        )

        self.mesh.bind_group = self.device.create_bind_group(bindGroupDesc)
