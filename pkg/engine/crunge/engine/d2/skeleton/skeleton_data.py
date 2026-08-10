# skeleton_data.py — immutable, loaded once from Spine JSON

class BoneData:
    def __init__(self, name, parent_index, x, y, rotation, scale_x=1.0, scale_y=1.0, length=0.0):
        self.name = name
        self.parent_index = parent_index  # -1 for root
        self.x, self.y = x, y             # local offset from parent, in units
        self.rotation = rotation          # degrees, local
        self.scale_x, self.scale_y = scale_x, scale_y
        self.length = length

class RegionAttachment:
    def __init__(self, path, x, y, rotation, scale_x, scale_y, width, height):
        self.path = path
        self.x, self.y, self.rotation = x, y, rotation
        self.scale_x, self.scale_y = scale_x, scale_y
        self.width, self.height = width, height  # in units, post-PPU

class SlotData:
    def __init__(self, name, bone_index, attachment_name=None):
        self.name = name
        self.bone_index = bone_index
        self.attachment_name = attachment_name

class SkeletonData:
    def __init__(self):
        self.bones: list[BoneData] = []
        self.slots: list[SlotData] = []
        self.skins: dict[str, dict[str, RegionAttachment]] = {}  # skin_name -> {slot_name: attachment}
        self.animations: dict[str, "Animation"] = {}

    @classmethod
    def from_spine_json(cls, path):
        # TODO: parse, ASSUMPTION on exact Spine 4.x schema until we check a real export
        ...


# skeleton_vu.py — render bridge, Skia-backed
'''
class SkeletonVu(Node2D):
    def __init__(self, skeleton: Skeleton):
        super().__init__()
        self.skeleton = skeleton

    def render(self, canvas):
        for slot in self.skeleton.slots:
            att = slot.attachment
            if att is None:
                continue
            world = slot.bone.world  # mat3, already composed with attachment offset later
            # draw quad for RegionAttachment via canvas.drawImageRect w/ world as local-to-world xform
            ...
'''