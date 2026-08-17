# skeleton.py — revised Bone / Skeleton with mutable pose fields

from loguru import logger
import glm

from .skeleton_data import BoneData, SlotData, RegionAttachment, SkeletonData


class Bone:
    def __init__(self, data: BoneData, parent: "Bone | None"):
        self.data = data
        self.parent = parent

        # Mutable per-frame pose, reset to setup values each apply() pass,
        # then mutated in place by timelines, then composed once into
        # `local` by Skeleton.update_world_transforms(). This is the piece
        # the timeline classes were missing something to write into.
        self.x = data.x
        self.y = data.y
        self.rotation = data.rotation
        self.scale_x = data.scale_x
        self.scale_y = data.scale_y

        self.local = glm.mat3(1.0)
        self.world = glm.mat3(1.0)

    def set_to_setup_pose(self):
        self.x = self.data.x
        self.y = self.data.y
        self.rotation = self.data.rotation
        self.scale_x = self.data.scale_x
        self.scale_y = self.data.scale_y

    def compose_local(self):
        """Build `local` from the current x/y/rotation/scale_x/scale_y.
        Called once per bone per frame, after all timelines have written
        into the pose fields above."""
        c = glm.cos(glm.radians(self.rotation))
        s = glm.sin(glm.radians(self.rotation))
        # translate * rotate * scale, column-major glm convention
        self.local = glm.mat3(
            c * self.scale_x,
            s * self.scale_x,
            0.0,
            -s * self.scale_y,
            c * self.scale_y,
            0.0,
            self.x,
            self.y,
            1.0,
        )


class Slot:
    def __init__(self, data: SlotData, bone: Bone):
        self.data = data
        self.bone = bone
        self.attachment: RegionAttachment | None = None
        #self.color = glm.vec4(1.0)
        self.color = self.data.color
        self.sequence_index = 0

    def set_to_setup_pose(self):
        skin = self.bone_owner_skeleton_skin  # ASSUMPTION placeholder, see note below
        self.attachment = (
            skin.get(self.data.attachment_name) if self.data.attachment_name else None
        )
        #self.color = glm.vec4(1.0)
        self.color = self.data.color



class Skeleton:
    def __init__(self, skeleton_data: SkeletonData, skin_name: str = "default"):
        self.data = skeleton_data
        self.current_skin_name = skin_name
        self.draw_order: list[int] | None = None  # None = data order
        self.event_listeners: list = []  # Callable[[str, int, float, str], None]

        self.bones: list[Bone] = []
        for bd in skeleton_data.bones:
            parent = self.bones[bd.parent_index] if bd.parent_index >= 0 else None
            self.bones.append(Bone(bd, parent))

        self.slots: list[Slot] = [
            Slot(sd, self.bones[sd.bone_index]) for sd in skeleton_data.slots
        ]

        self.set_skin(skin_name)

    def fire_event(self, name, int_value, float_value, string_value):
        for listener in self.event_listeners:
            listener(name, int_value, float_value, string_value)

    def _resolve_attachment(self, slot):
        """Skin-specific attachment wins; fall back to the default skin,
        which holds attachments shared across all skins (goblins keeps the
        shield and spear there while body parts live in goblin/goblingirl)."""
        if not slot.data.attachment_name:
            return None
        skin = self.data.skins.get(self.current_skin_name, {})
        attachment = skin.get(slot.data.name, {}).get(slot.data.attachment_name)
        if attachment is None and self.current_skin_name != "default":
            default_skin = self.data.skins.get("default", {})
            attachment = default_skin.get(slot.data.name, {}).get(
                slot.data.attachment_name
            )
        return attachment

    def set_skin(self, name):
        self.current_skin_name = name
        for slot in self.slots:
            slot.attachment = self._resolve_attachment(slot)

    def set_to_setup_pose(self):
        for bone in self.bones:
            bone.set_to_setup_pose()
        for slot in self.slots:
            slot.attachment = self._resolve_attachment(slot)
            slot.color = slot.data.color
            slot.sequence_index = (
                slot.attachment.sequence.setupIndex
                if slot.attachment is not None and slot.attachment.sequence is not None
                else 0
            )
        self.draw_order = None

    """
    def set_skin(self, name):
        self.current_skin_name = name
        logger.debug(name)
        self.skin = self.data.skins[name]
        for slot in self.slots:
            slot_attachments = self.skin.get(slot.data.name, {})
            slot.attachment = slot_attachments.get(slot.data.attachment_name) if slot.data.attachment_name else None

    def set_to_setup_pose(self):
        for bone in self.bones:
            bone.set_to_setup_pose()
        skin = self.data.skins[self.current_skin_name]
        for slot in self.slots:
            slot_attachments = skin.get(slot.data.name, {})
            slot.attachment = (
                slot_attachments.get(slot.data.attachment_name)
                if slot.data.attachment_name
                else None
            )
            slot.color = glm.vec4(1.0)
            slot.sequence_index = (
                slot.attachment.sequence.setupIndex
                if slot.attachment is not None and slot.attachment.sequence is not None
                else 0
            )
    """

    def update_world_transforms(self):
        for bone in self.bones:  # parent-first order guaranteed by BoneData ordering
            bone.compose_local()
            bone.world = (
                bone.local if bone.parent is None else bone.parent.world * bone.local
            )
