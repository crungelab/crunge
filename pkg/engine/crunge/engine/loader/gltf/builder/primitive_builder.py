from loguru import logger

import numpy as np
import glm

from crunge import wgpu
from crunge import gltf

#from ..constants import SAMPLE_COUNT
from ..debug import (
    debug_accessor,
    debug_material,
)

from ....d3.primitive_3d import Primitive3D, Primitive3DProgram
from ....d3.material_3d import Material3D

from ..normals import compute_normals

from . import GltfBuilder
from .builder_context import BuilderContext
from .vertex_table import VertexTable
from .vertex_column import PosColumn, NormalColumn, UvColumn, RgbaColumn, TangentColumn
from .material_builder import MaterialBuilder
from .program_builder import ProgramBuilder


class PrimitiveBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, tf_primitive: gltf.Primitive) -> None:
        super().__init__(context)
        self.tf_primitive = tf_primitive
        self.primitive = Primitive3D()
        self.program = Primitive3DProgram()
        self.material: Material3D = None
        self.vertex_table = VertexTable()

    def build(self):
        self.build_indices()
        self.build_material()
        self.build_attributes()
        self.build_program()

        vertex_data = self.vertex_table.data

        self.primitive.vertex_data = vertex_data
        self.primitive.vertex_buffer = self.gfx.create_buffer_from_ndarray(
            "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

        return self.primitive

    def build_attributes(self):
        tf_primitive = self.tf_primitive
        attributes: dict = tf_primitive.attributes
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
                tangents = gltf.compute_tangents(
                    self.primitive.index_data,
                    self.vertex_table.get("pos").data,
                    self.vertex_table.get("uv").data,
                    self.vertex_table.get("normal").data,
                )
                self.vertex_table.add_column(TangentColumn("tangent", tangents))

    def build_attribute(self, attribute: tuple[str, int]):
        name, accessor_index = attribute
        logger.debug(f"primitive.attributes[{name}]: {accessor_index}")
        accessor = self.tf_model.accessors[accessor_index]
        # data = self.build_attribute_array(index)
        data = self.build_array(accessor_index)

        if name == "POSITION":
            self.vertex_table.add_column(PosColumn("pos", data))
            min_values = accessor.min_values
            max_values = accessor.max_values
            min = glm.vec3(min_values[0], min_values[1], min_values[2])
            max = glm.vec3(max_values[0], max_values[1], max_values[2])
            self.primitive.bounds.min = min
            self.primitive.bounds.max = max

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
            raise Exception(f"Unknown attribute: {name}")

        # logger.debug(f"data: {data}")

    def build_indices(self):
        tf_primitive = self.tf_primitive
        logger.debug(f"primitive.indices: {tf_primitive.indices}")
        accessor = self.tf_model.accessors[tf_primitive.indices]
        # debug_accessor(accessor)

        indices = self.build_array(tf_primitive.indices)
        # logger.debug(f"indices: {indices}")

        component_type = accessor.component_type
        logger.debug(f"component_type: {component_type}")
        if component_type == gltf.ComponentType.UNSIGNED_SHORT:
            self.primitive.index_format = wgpu.IndexFormat.UINT16
        elif component_type == gltf.ComponentType.UNSIGNED_INT:
            self.primitive.index_format = wgpu.IndexFormat.UINT32
        elif component_type == gltf.ComponentType.UNSIGNED_BYTE:
            indices = np.array(indices, dtype=np.uint16)
            self.primitive.index_format = wgpu.IndexFormat.UINT16

        self.primitive.index_data = indices
        self.primitive.index_buffer = self.gfx.create_buffer_from_ndarray(
            "INDEX", indices, wgpu.BufferUsage.INDEX
        )

    def build_array(self, accessor_index: int):
        if accessor_index in self.context.array_cache:
            return self.context.array_cache[accessor_index]

        accessor = self.tf_model.accessors[accessor_index]
        # debug_accessor(accessor)

        buffer_view = self.tf_model.buffer_views[accessor.buffer_view]
        buffer = self.tf_model.buffers[buffer_view.buffer]
        logger.debug(f"buffer_view: {buffer_view}")
        logger.debug(f"buffer: {buffer}")

        type = accessor.type
        logger.debug(f"type: {type}")

        component_type = accessor.component_type
        logger.debug(f"component_type: {component_type}")

        count = accessor.count
        logger.debug(f"count: {count}")
        array = buffer.get_array(
            buffer_view.byte_offset + accessor.byte_offset, count, type, component_type
        )
        self.context.array_cache[accessor_index] = array
        return array

    '''
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
    '''

    def build_material(self):
        if self.tf_primitive.material < 0:
            return
        tf_primitive = self.tf_primitive
        logger.debug(f"primitive.material: {tf_primitive.material}")
        self.material = MaterialBuilder(self.context, tf_primitive.material).build()
        self.primitive.material = self.material

    def build_program(self):
        if not self.material.alpha_mode == "BLEND":
            logger.debug("Creating Program for OPAQUE/MASK material")
            self.primitive.program = ProgramBuilder(self.context, self.vertex_table, self.material).build()
            return
        
        logger.debug("Creating Program for BLEND material")
        self.primitive.program = ProgramBuilder(self.context, self.vertex_table, self.material, write_color=False).build()
        self.primitive.deferred_program = ProgramBuilder(self.context, self.vertex_table, self.material, write_depth=False).build()
    