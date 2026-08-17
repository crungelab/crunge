# skeleton_vu.py

from loguru import logger
import glm

from ..node_2d import Node2D
from ..vu_2d import Vu2D
from ..sprite.sprite_vu import SpriteVu
from ..sprite.sprite_program import AdditiveSpriteProgram

from .skeleton import Skeleton


def _mat3_to_mat4(m3: glm.mat3) -> glm.mat4:
    return glm.mat4(
        m3[0][0],
        m3[0][1],
        0.0,
        0.0,
        m3[1][0],
        m3[1][1],
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        m3[2][0],
        m3[2][1],
        0.0,
        1.0,
    )


def _attachment_local_mat4(att) -> glm.mat4:
    """RegionAttachment's own offset/rotation/scale relative to its bone,
    plus sizing the unit quad to the attachment's actual width/height.
    Mirrors Vu2D.on_node_transform_change's scale-by-size step, which
    update_pose() was skipping entirely."""
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(att.x, att.y, 0.0))
    m = glm.rotate(m, glm.radians(att.rotation), glm.vec3(0, 0, 1))
    m = glm.scale(
        m,
        glm.vec3(
            att.width * att.scale_x,
            att.height * att.scale_y,
            1.0,
        ),
    )
    return m


def _centering_offset_mat4(skeleton_data) -> glm.mat4:
    """Shift skeleton-space origin so the artist's bounding box is centered
    on the node, rather than rendering at whatever arbitrary point the rig's
    root bone happens to sit (feet, hips, etc. depending on the asset)."""
    cx = skeleton_data.bounds_x + skeleton_data.bounds_width / 2.0
    cy = skeleton_data.bounds_y + skeleton_data.bounds_height / 2.0
    return glm.translate(glm.mat4(1.0), glm.vec3(-cx, -cy, 0.0))


class SkeletonVu(Vu2D):
    def __init__(self, skeleton: Skeleton = None) -> None:
        super().__init__()
        self.skeleton = skeleton
        self._centering = (
            _centering_offset_mat4(skeleton.data) if skeleton else glm.mat4(1.0)
        )

        self.anim_state = None
        self.manual_draw = True

        self._slot_vus: list[SpriteVu] = []
        self._last_attachment: list[object] = []

        if skeleton is not None:
            self._build_slot_vus()

    def _build_slot_vus(self):
        self._slot_vus = []
        self._last_sprite = [None] * len(self.skeleton.slots)

        for i, slot in enumerate(self.skeleton.slots):
            slot_vu = SpriteVu()

            if slot.data.blend_mode == "additive":
                logger.debug(f"Slot '{slot.data.name}' using additive blend mode")
                slot_vu.program = AdditiveSpriteProgram()

            slot_vu.enable()

            '''
            if slot.data.blend_mode == "additive":
                logger.debug(f"Slot '{slot.data.name}' using additive blend mode")
                slot_vu.program = AdditiveSpriteProgram()
            '''

            att = slot.attachment
            if att is not None:
                sprite = (
                    att.sequence_sprites[slot.sequence_index]
                    if att.sequence_sprites
                    else att.gpu_sprite
                )
                if sprite is not None:
                    slot_vu.sprite = sprite
                    self._last_sprite[i] = sprite
                else:
                    logger.warning(
                        f"Slot '{slot.data.name}' has attachment "
                        f"'{att.path}' with no resolved sprite — "
                        f"atlas.resolve() may not have found a matching region"
                    )

            self._slot_vus.append(slot_vu)

    def on_node_transform_change(self, node: Node2D) -> None:
        self.transform = node.transform
        self.bounds = node.bounds  # TODO: union of slot bounds, not the raw node bounds

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0)  # unused — on_node_transform_change is overridden above

    """
    def update(self, delta_time: float):
        self.update_pose()
    """

    def update_pose(self):
        root = self.transform * self._centering

        for i, slot in enumerate(self.skeleton.slots):
            att = slot.attachment
            if att is None:
                # Clear tracking so _draw() stops drawing the previous sprite —
                # otherwise a blink leaves the eyelid hanging at its last transform.
                self._last_sprite[i] = None
                continue

            if att.sequence_sprites:
                sprite = att.sequence_sprites[slot.sequence_index]
            else:
                sprite = att.gpu_sprite

            if sprite is None:
                self._last_sprite[i] = None
                continue

            slot_vu = self._slot_vus[i]

            if sprite is not self._last_sprite[i]:
                slot_vu.sprite = sprite
                self._last_sprite[i] = sprite

            slot_vu._color = (
                slot.color
            )  # bypass setter; transform assignment below triggers the single upload
            bone_world4 = _mat3_to_mat4(slot.bone.world)
            attachment_local4 = _attachment_local_mat4(att)
            slot_vu.transform = root * bone_world4 * attachment_local4

    def _draw(self):
        order = self.skeleton.draw_order or range(len(self.skeleton.slots))
        for i in order:
            if self._last_sprite[i] is not None:
                self._slot_vus[i].draw()
