# skeleton_vu.py

from loguru import logger
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

def _attachment_local_mat4(att) -> glm.mat4:
    """RegionAttachment's own offset/rotation/scale relative to its bone,
    plus sizing the unit quad to the attachment's actual width/height.
    Mirrors Vu2D.on_node_transform_change's scale-by-size step, which
    update_pose() was skipping entirely."""
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(att.x, att.y, 0.0))
    m = glm.rotate(m, glm.radians(att.rotation), glm.vec3(0, 0, 1))
    m = glm.scale(m, glm.vec3(
        att.width * att.scale_x,
        att.height * att.scale_y,
        1.0,
    ))
    return m

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

        for i, slot in enumerate(self.skeleton.slots):
            slot_vu = SpriteVu()
            slot_vu.enable()

            # Skeleton.__init__ already ran set_skin(), so slot.attachment may
            # already be populated from the setup pose by the time SkeletonVu
            # is constructed. Seed it here instead of waiting for the first
            # update_pose() dirty-check, which only fires on *changes*.
            if slot.attachment is not None:
                if slot.attachment.gpu_sprite is not None:
                    slot_vu.sprite = slot.attachment.gpu_sprite
                    self._last_attachment[i] = slot.attachment
                else:
                    logger.warning(
                        f"Slot '{slot.data.name}' has attachment "
                        f"'{slot.attachment.path}' with no resolved gpu_sprite — "
                        f"atlas.resolve() may not have found a matching region"
                    )

            self._slot_vus.append(slot_vu)
    '''
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
    '''

    def on_node_transform_change(self, node: Node2D) -> None:
        self.transform = node.transform
        self.bounds = node.bounds  # TODO: union of slot bounds, not the raw node bounds

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0)  # unused — on_node_transform_change is overridden above

    def update_pose(self):
        root = self.transform

        for i, slot in enumerate(self.skeleton.slots):
            if slot.attachment is None or slot.attachment.gpu_sprite is None:
                continue

            slot_vu = self._slot_vus[i]

            if slot.attachment is not self._last_attachment[i]:
                slot_vu.sprite = slot.attachment.gpu_sprite
                self._last_attachment[i] = slot.attachment

            bone_world4 = _mat3_to_mat4(slot.bone.world)
            attachment_local4 = _attachment_local_mat4(slot.attachment)
            slot_vu.transform = root * bone_world4 * attachment_local4

    def _draw(self):
        for i, slot in enumerate(self.skeleton.slots):
            if slot.attachment is not None and slot.attachment.gpu_sprite is not None:
                self._slot_vus[i].draw()
