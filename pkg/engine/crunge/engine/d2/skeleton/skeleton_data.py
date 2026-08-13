# skeleton_data.py — immutable, loaded once from Spine JSON

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .animation import Animation


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


"""
class RegionAttachment:
    def __init__(self, path, x, y, rotation, scale_x, scale_y, width, height):
        self.path = path
        self.x, self.y, self.rotation = x, y, rotation
        self.scale_x, self.scale_y = scale_x, scale_y
        self.width, self.height = width, height  # in units, post-PPU
"""


class SlotData:
    def __init__(self, name, bone_index, attachment_name=None):
        self.name = name
        self.bone_index = bone_index
        self.attachment_name = attachment_name


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
