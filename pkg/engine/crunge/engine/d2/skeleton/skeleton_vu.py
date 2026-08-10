# skeleton_vu.py

import glm
from ..node_2d import Node2D
from ..vu_2d import Vu2D
from ..sprite.sprite_vu import SpriteVu

from .skeleton import Skeleton

def _mat3_to_mat4(m3: glm.mat3) -> glm.mat4:
    return glm.mat4(
        m3[0][0], m3[0][1], 0.0, 0.0,
        m3[1][0], m3[1][1], 0.0, 0.0,
        0.0,      0.0,      1.0, 0.0,
        m3[2][0], m3[2][1], 0.0, 1.0,
    )


class SkeletonVu(Vu2D):
    def __init__(self, skeleton: Skeleton = None) -> None:
        super().__init__()
        self.skeleton = skeleton
        self.anim_state = None
        self.manual_draw = True

        self._slot_vus: list[SpriteVu] = []
        self._last_attachment: list[object] = []

        if skeleton is not None:
            self._build_slot_vus()

    def _build_slot_vus(self):
        self._slot_vus = []
        self._last_attachment = [None] * len(self.skeleton.slots)

        for _ in self.skeleton.slots:
            slot_vu = SpriteVu()
            # These children never get a Node2D of their own (they're driven
            # directly by bone.world in update_pose(), not the Node listener
            # mechanism) so .node is never set. But they still need the
            # normal Base lifecycle — .enable() both creates (allocates
            # program/buffers/bind_groups via Vu2D._create) and sets
            # enabled=True, which Vu2D.on_transform() requires before it will
            # call update_gpu() at all. Skipping this was the bug in the
            # previous draft: transform assignment would have silently no-op'd.
            slot_vu.enable()
            self._slot_vus.append(slot_vu)

    def on_node_transform_change(self, node: Node2D) -> None:
        self.transform = node.transform
        self.bounds = node.bounds  # TODO: union of slot bounds, not the raw node bounds

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0)  # unused — on_node_transform_change is overridden above

    def update_pose(self):
        """Call after anim_state.apply() each frame."""
        root = self.transform

        for i, slot in enumerate(self.skeleton.slots):
            if slot.attachment is None:
                continue

            slot_vu = self._slot_vus[i]

            if slot.attachment is not self._last_attachment[i]:
                slot_vu.sprite = slot.attachment.gpu_sprite  # still blocked on the atlas loader
                self._last_attachment[i] = slot.attachment

            slot_vu.transform = root * _mat3_to_mat4(slot.bone.world)

    def _draw(self):
        for i, slot in enumerate(self.skeleton.slots):
            if slot.attachment is not None:
                self._slot_vus[i].draw()  # public entry point, not _draw() directly