from loguru import logger

from crunge import gltf

from crunge.engine.d3.mesh_3d import Mesh3D

from ..debug import (
    debug_mesh,
)

from . import GltfBuilder
from .builder_context import BuilderContext

from .primitive_builder import PrimitiveBuilder


class MeshBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, mesh_index: int) -> None:
        super().__init__(context)
        self.mesh_index = mesh_index
        self.tf_mesh: gltf.Mesh = None
        self.mesh: Mesh3D = None

    def build(self) -> Mesh3D:
        if self.mesh_index in self.context.mesh_cache:
            mesh = self.context.mesh_cache[self.mesh_index]
            return mesh

        self.tf_mesh: gltf.Mesh = self.tf_model.meshes[self.mesh_index]

        logger.debug(f"Building Mesh: {self.tf_mesh.name} (index: {self.mesh_index})")

        self.mesh = mesh = Mesh3D()
        self.build_primitives()
        self.context.mesh_cache[self.mesh_index] = mesh
        return mesh

    def build_primitives(self):
        for tf_primitive in self.tf_mesh.primitives:
            primitive_builder = PrimitiveBuilder(self.context, tf_primitive)
            primitive = primitive_builder.build()
            self.mesh.add_primitive(primitive)
