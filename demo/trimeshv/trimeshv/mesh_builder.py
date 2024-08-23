import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm

from crunge import wgpu
from crunge.wgpu import utils

from .builder import Builder
from .scene import Scene
from .mesh import Mesh

from .vertex_table import VertexTable
from .vertex_column import PosColumn, NormalColumn, UvColumn, RgbaColumn

from .material_builder import MaterialBuilder
from .material import Material

from .shader import VertexShaderBuilder, FragmentShaderBuilder


class MeshBuilder(Builder):
    mesh: Mesh = None
    vertex_table: VertexTable = None
    material: Material = None

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.mesh = Mesh()
        self.vertex_table = VertexTable()

    def build(self, tm_mesh: tm.Trimesh):
        logger.debug("Building mesh")
        mesh: Mesh = self.mesh
        logger.debug(tm_mesh.__dict__)

        # Vertices
        vertices = tm_mesh.vertices.astype(np.float32)
        self.vertex_table.add_column(PosColumn("pos", vertices))

        # Normals
        normals = tm_mesh.vertex_normals.astype(np.float32)
        self.vertex_table.add_column(NormalColumn("normal", normals))

        # Visuals
        visual = tm_mesh.visual
        visual_kind = visual.kind
        logger.debug(f"visual_kind:  {visual_kind}")
        if visual_kind == "texture":
            if hasattr(visual, "uv") and visual.uv is not None:
                uv_coords = visual.uv.astype(np.float32)
                '''
                min_values = np.array(np.min(uv_coords), dtype=np.float32)
                logger.debug(f"min_values: {min_values}")
                max_values = np.array(np.max(uv_coords), dtype=np.float32)
                logger.debug(f"max_values: {max_values}")
                uv_coords = uv_coords - min_values
                #logger.debug(data)

                # Now, scale the values so the maximum becomes 1
                range_values = max_values - min_values
                logger.debug(f"range_values: {range_values}")
                uv_coords = uv_coords / range_values
                #logger.debug(uv_coords)
                '''
                self.vertex_table.add_column(UvColumn("uv", uv_coords))

        elif visual_kind == "vertex":
            vc = visual.vertex_colors.astype(np.float32)
            self.vertex_table.add_column(RgbaColumn("color", vc))

        # Vertex Data
        vertex_data = self.vertex_table.data

        mesh.vertex_data = vertex_data
        mesh.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

        # exit()

        # Indices
        indices = tm_mesh.faces.astype(np.uint32)
        # logger.debug(f"indices:  {indices}")
        n_indices = self.n_indices = len(indices)
        logger.debug(f"n_indices:  {n_indices}")
        mesh.index_data = indices
        mesh.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", indices, wgpu.BufferUsage.INDEX
        )

        # Uniform Buffer

        uniform_buffer_size = 4 * 16
        mesh.uniform_buffer_size = uniform_buffer_size

        uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        mesh.uniform_buffer = uniform_buffer

        visual = tm_mesh.visual
        logger.debug(visual.__dict__)

        if visual.kind == "texture":
            tm_material = visual.material
            logger.debug(tm_material.__dict__)

            material = MaterialBuilder().build(tm_material)
            self.material = material
        elif visual.kind == "vertex":
            material = Material()
            material.base_color_factor = (1, 1, 1, 1)
            self.material = material

        pipeline = self.create_pipeline()
        mesh.pipeline = pipeline

        bg_entries = [
            wgpu.BindGroupEntry(
                binding=0, buffer=uniform_buffer, size=uniform_buffer_size
            ),
        ]

        for i, texture in enumerate(material.textures):
            bg_entries.append(
                wgpu.BindGroupEntry(binding=i * 2 + 1, sampler=texture.sampler)
            )
            bg_entries.append(
                wgpu.BindGroupEntry(binding=i * 2 + 2, texture_view=texture.view)
            )

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Uniform bind group",
            layout=pipeline.get_bind_group_layout(0),
            entry_count=len(bg_entries),
            entries=bg_entries,
        )

        mesh.bind_group = self.device.create_bind_group(bindGroupDesc)

        return mesh

    def create_vertex_attributes(self):
        logger.debug("Creating vertex attributes")
        vert_attributes = wgpu.VertexAttributes()
        offset = 0
        for i, column in enumerate(self.vertex_table.columns):
            vert_attributes.append(
                wgpu.VertexAttribute(
                    format=column.format,
                    offset=offset,
                    shader_location=i,
                )
            )
            offset += column.struct_size
        return vert_attributes

    def create_pipeline(self):
        logger.debug("Creating pipeline")
        vs_module: wgpu.ShaderModule = VertexShaderBuilder(self.vertex_table).build()
        fs_module: wgpu.ShaderModule = FragmentShaderBuilder(
            self.vertex_table, self.material
        ).build()

        vertAttributes = self.create_vertex_attributes()

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

        """
        wgpu::BlendState blend_state = {};
        blend_state.alpha.operation = wgpu::BlendOperation::Add;
        blend_state.alpha.srcFactor = wgpu::BlendFactor::One;
        blend_state.alpha.dstFactor = wgpu::BlendFactor::OneMinusSrcAlpha;
        blend_state.color.operation = wgpu::BlendOperation::Add;
        blend_state.color.srcFactor = wgpu::BlendFactor::SrcAlpha;
        blend_state.color.dstFactor = wgpu::BlendFactor::OneMinusSrcAlpha;
        """
        if self.material.alpha_mode == "BLEND":
            blend_state = wgpu.BlendState(
                alpha=wgpu.BlendComponent(
                    operation=wgpu.BlendOperation.ADD,
                    src_factor=wgpu.BlendFactor.ONE,
                    dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
                    # dst_factor=wgpu.BlendFactor.ONE,
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
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            )
        ]

        for i, texture in enumerate(self.material.textures):
            bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + 1,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    sampler=wgpu.SamplerBindingLayout(
                        type=wgpu.SamplerBindingType.FILTERING
                    ),
                )
            )
            bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + 2,
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

        return self.device.create_render_pipeline(rp_descriptor)
