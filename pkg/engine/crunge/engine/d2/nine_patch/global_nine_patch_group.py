from crunge.core import klass

from ..uniforms_2d import NinePatchUniform
from ...buffer import UniformBuffer
from ..binding_2d import ModelBindGroup

from .nine_patch import NinePatch, NinePatchMembership
from .nine_patch_group import NinePatchGroup


@klass.singleton
class GlobalNinePatchGroup(NinePatchGroup):
    def __init__(self):
        super().__init__()
        self.is_dynamic_group = False

    def create_membership(self, nine_patch: NinePatch) -> NinePatchMembership:
        buffer = UniformBuffer(NinePatchUniform, 1, label="Nine Patch Model Buffer")
        bind_group = ModelBindGroup(
            buffer.get(),
            buffer.size,
        )

        membership = NinePatchMembership(self, nine_patch, 0, buffer, bind_group)
        return membership
