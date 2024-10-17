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
    def __init__(self, context: BuilderContext, index: int) -> None:
        super().__init__(context)
        self.index = index
        self.tf_mesh: gltf.Mesh = None
        self.mesh: Mesh3D = None

    def build(self) -> Mesh3D:
        if self.index in self.context.mesh_cache:
            self.mesh = self.context.mesh_cache[self.index]
            return self.mesh

        self.tf_mesh: gltf.Mesh = self.tf_model.meshes[self.index]
        self.mesh = Mesh3D()
        self.build_primitives()
        self.context.mesh_cache[self.index] = self.mesh
        return self.mesh

    def build_primitives(self):
        for tf_primitive in self.tf_mesh.primitives:
            primitive_builder = PrimitiveBuilder(self.context, tf_primitive)
            primitive = primitive_builder.build()
            self.mesh.add_primitive(primitive)
