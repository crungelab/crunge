# skeleton_data.py — immutable, loaded once from Spine JSON

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .animation import Animation

import glm


class BoneData:
    def __init__(
        self, name, parent_index, x, y, rotation, scale_x=1.0, scale_y=1.0, length=0.0
    ):
        self.name = name
        self.parent_index = parent_index  # -1 for root
        self.x, self.y = x, y  # local offset from parent, in units
        self.rotation = rotation  # degrees, local
        self.scale_x, self.scale_y = scale_x, scale_y
        self.length = length


class RegionAttachment:
    def __init__(
        self, path, x, y, rotation, scale_x, scale_y, width, height, sequence=None
    ):
        self.path = path
        self.x, self.y, self.rotation = x, y, rotation
        self.scale_x, self.scale_y = scale_x, scale_y
        self.width, self.height = width, height  # in units, post-PPU

        self.sequence = sequence  # SequenceJSON | None
        self.gpu_sprite = None  # non-sequence case
        self.sequence_sprites: list = []  # frame-indexed, empty if not a sequence

    def __repr__(self):
        return (
            f"RegionAttachment(path={self.path!r}, x={self.x}, y={self.y}, "
            f"rotation={self.rotation}, scale_x={self.scale_x}, scale_y={self.scale_y}, "
            f"width={self.width}, height={self.height}, sequence={self.sequence!r})"
        )


class SlotData:
    def __init__(
        self, name, bone_index, attachment_name=None, color=None, blend_mode="normal"
    ):
        self.name = name
        self.bone_index = bone_index
        self.attachment_name = attachment_name
        self.color = color if color is not None else glm.vec4(1.0)
        self.blend_mode = blend_mode


"""
class SlotData:
    def __init__(self, name, bone_index, attachment_name=None, color=glm.vec4(1.0)):
        self.name = name
        self.bone_index = bone_index
        self.attachment_name = attachment_name
        self.color = color
"""


class EventData:
    def __init__(self, name, int_value=0, float_value=0.0, string_value=""):
        self.name = name
        self.int_value = int_value
        self.float_value = float_value
        self.string_value = string_value


class SkeletonData:
    def __init__(self):
        self.bones: list[BoneData] = []
        self.slots: list[SlotData] = []
        self.skins: dict[str, dict[str, RegionAttachment]] = (
            {}
        )  # skin_name -> {slot_name: attachment}
        self.animations: dict[str, "Animation"] = {}

        self.bounds_x = 0.0
        self.bounds_y = 0.0
        self.bounds_width = 0.0
        self.bounds_height = 0.0

        self.events: dict[str, EventData] = {}
