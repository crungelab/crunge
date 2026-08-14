# spine_converter.py — SpineSkeletonFile -> SkeletonData

from __future__ import annotations

from loguru import logger
import glm

from crunge.engine.d2.settings_2d import (
    Settings2D,
)  # ASSUMPTION: import path, confirm against actual module layout

from .spine_json import (
    SpineSkeletonFile,
    BoneJSON,
    SlotJSON,
    SkinJSON,
    RegionAttachmentJSON,
    AnimationJSON,
)
from crunge.engine.d2.skeleton.skeleton_data import (
    SkeletonData,
    BoneData,
    SlotData,
    RegionAttachment,
)
from crunge.engine.d2.skeleton.animation import (
    Animation,
    RotateTimeline,
    TranslateTimeline,
    ScaleTimeline,
    AttachmentTimeline,
    SequenceTimeline,
)


def _parse_curve(curve) -> str | tuple[float, float, float, float]:
    """Normalize Spine's curve field: None -> "linear", "stepped" -> "stepped",
    [cx1,cy1,cx2,cy2] -> bezier tuple. Actual sampling logic comes later."""
    if curve is None:
        return "linear"
    if isinstance(curve, str):
        return "stepped"
    return tuple(curve)  # bezier control points


# spine_converter.py

def _region_attachment(name: str, data: dict, ppu: float) -> RegionAttachment:
    att = RegionAttachmentJSON.model_validate(data)
    return RegionAttachment(
        # path wins; then the attachment's own name field; then the dict key.
        # goblins uses the middle case: key "eyes-closed", name "goblin/eyes-closed".
        path=att.path or att.name or name,
        x=att.x / ppu,
        y=att.y / ppu,
        rotation=att.rotation,
        scale_x=att.scaleX,
        scale_y=att.scaleY,
        width=att.width / ppu,
        height=att.height / ppu,
        sequence=att.sequence,
    )

"""
def _region_attachment(name: str, data: dict, ppu: float) -> RegionAttachment:
    att = RegionAttachmentJSON.model_validate(data)
    return RegionAttachment(
        path=att.path or name,
        x=att.x / ppu,
        y=att.y / ppu,
        rotation=att.rotation,
        scale_x=att.scaleX,
        scale_y=att.scaleY,
        width=att.width / ppu,
        height=att.height / ppu,
        sequence=att.sequence,
    )
"""


def convert(spine_file: SpineSkeletonFile, ppu: float | None = None) -> SkeletonData:
    if ppu is None:
        ppu = Settings2D().ppu

    result = SkeletonData()

    result.bounds_x = spine_file.skeleton.x / ppu
    result.bounds_y = spine_file.skeleton.y / ppu
    result.bounds_width = spine_file.skeleton.width / ppu
    result.bounds_height = spine_file.skeleton.height / ppu

    # --- bones: Spine guarantees parent-before-child ordering already ---
    bone_index_by_name: dict[str, int] = {}
    for i, b in enumerate(spine_file.bones):
        bone_index_by_name[b.name] = i
        parent_index = bone_index_by_name[b.parent] if b.parent else -1
        result.bones.append(
            BoneData(
                name=b.name,
                parent_index=parent_index,
                x=b.x / ppu,
                y=b.y / ppu,
                rotation=b.rotation,
                scale_x=b.scaleX,
                scale_y=b.scaleY,
                length=b.length / ppu,
            )
        )

    # --- slots ---
    slot_index_by_name: dict[str, int] = {}
    for i, s in enumerate(spine_file.slots):
        slot_index_by_name[s.name] = i
        result.slots.append(
            SlotData(
                name=s.name,
                bone_index=bone_index_by_name[s.bone],
                attachment_name=s.attachment,
            )
        )

    # --- skins: skin_name -> {slot_name: {attachment_name: attachment}} ---
    for skin in spine_file.skins:
        skin_out: dict[str, dict[str, RegionAttachment]] = {}
        for slot_name, attachments in skin.attachments.items():
            skin_out[slot_name] = {}
            for att_name, att_data in attachments.items():
                att_type = att_data.get("type", "region")
                if att_type != "region":
                    continue
                skin_out[slot_name][att_name] = _region_attachment(
                    att_name, att_data, ppu
                )
        result.skins[skin.name] = skin_out

    # --- animations ---
    for anim_name, anim in spine_file.animations.items():
        timelines = []

        for bone_name, bone_tl in anim.bones.items():
            bone_index = bone_index_by_name[bone_name]

            if bone_tl.rotate:
                timelines.append(
                    RotateTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.value, _parse_curve(kf.curve))
                            for kf in bone_tl.rotate
                        ],
                    )
                )
            if bone_tl.translate:
                timelines.append(
                    TranslateTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.x / ppu, kf.y / ppu, _parse_curve(kf.curve))
                            for kf in bone_tl.translate
                        ],
                    )
                )
            if bone_tl.scale:
                timelines.append(
                    ScaleTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.x, kf.y, _parse_curve(kf.curve))
                            for kf in bone_tl.scale
                        ],
                    )
                )

        for slot_name, slot_tl in anim.slots.items():
            slot_index = slot_index_by_name[slot_name]
            if slot_tl.attachment:
                timelines.append(
                    AttachmentTimeline(
                        slot_index=slot_index,
                        keyframes=[(kf.time, kf.name) for kf in slot_tl.attachment],
                    )
                )

        # --- sequence timelines: skin_name -> slot_name -> attachment_name ---
        for skin_name, slots_in_skin in anim.attachments.items():
            skin_attachments = result.skins.get(skin_name)
            if skin_attachments is None:
                logger.warning(
                    f"Animation '{anim_name}' references unknown skin '{skin_name}'"
                )
                continue

            for slot_name, attachments in slots_in_skin.items():
                slot_index = slot_index_by_name.get(slot_name)
                if slot_index is None:
                    logger.warning(
                        f"Animation '{anim_name}' references unknown slot '{slot_name}'"
                    )
                    continue

                for att_name, att_tl in attachments.items():
                    if not att_tl.sequence:
                        continue

                    att = skin_attachments.get(slot_name, {}).get(att_name)
                    if att is None or att.sequence is None:
                        logger.warning(
                            f"Sequence timeline for '{slot_name}/{att_name}' in "
                            f"animation '{anim_name}' has no matching sequence "
                            f"attachment in skin '{skin_name}'"
                        )
                        continue

                    timelines.append(
                        SequenceTimeline(
                            slot_index=slot_index,
                            attachment=att,
                            keyframes=list(att_tl.sequence),
                        )
                    )

        duration = max(
            (
                kf.time
                for tl_group in [anim.bones.values(), anim.slots.values()]
                for tl in tl_group
                for kfs in (
                    getattr(tl, "rotate", []),
                    getattr(tl, "translate", []),
                    getattr(tl, "scale", []),
                    getattr(tl, "attachment", []),
                )
                for kf in kfs
            ),
            # Sequence keyframes live under anim.attachments, which the
            # comprehension above doesn't reach — fold them in as the
            # default so a sequence-only animation still gets a duration.
            default=max(
                (
                    kf.time
                    for slots_in_skin in anim.attachments.values()
                    for attachments in slots_in_skin.values()
                    for att_tl in attachments.values()
                    for kf in att_tl.sequence
                ),
                default=0.0,
            ),
        )

        result.animations[anim_name] = Animation(anim_name, duration, timelines)

    return result


"""
def convert(spine_file: SpineSkeletonFile, ppu: float | None = None) -> SkeletonData:
    if ppu is None:
        ppu = Settings2D().ppu

    result = SkeletonData()

    result.bounds_x = spine_file.skeleton.x / ppu
    result.bounds_y = spine_file.skeleton.y / ppu
    result.bounds_width = spine_file.skeleton.width / ppu
    result.bounds_height = spine_file.skeleton.height / ppu

    # --- bones: Spine guarantees parent-before-child ordering already ---
    bone_index_by_name: dict[str, int] = {}
    for i, b in enumerate(spine_file.bones):
        # logger.debug(f"bone: {b}")
        bone_index_by_name[b.name] = i
        parent_index = bone_index_by_name[b.parent] if b.parent else -1
        result.bones.append(
            BoneData(
                name=b.name,
                parent_index=parent_index,
                x=b.x / ppu,
                y=b.y / ppu,
                rotation=b.rotation,
                scale_x=b.scaleX,
                scale_y=b.scaleY,
                length=b.length / ppu,
            )
        )

    # --- slots ---
    slot_index_by_name: dict[str, int] = {}
    for i, s in enumerate(spine_file.slots):
        slot_index_by_name[s.name] = i
        result.slots.append(
            SlotData(
                name=s.name,
                bone_index=bone_index_by_name[s.bone],
                attachment_name=s.attachment,
            )
        )

    # --- skins: skin_name -> {slot_name: {attachment_name: attachment}} ---
    for skin in spine_file.skins:
        skin_out: dict[str, dict[str, RegionAttachment]] = (
            {}
        )  # slot_name -> attachment_name -> attachment
        for slot_name, attachments in skin.attachments.items():
            skin_out[slot_name] = {}
            for att_name, att_data in attachments.items():
                att_type = att_data.get("type", "region")
                if att_type != "region":
                    continue
                skin_out[slot_name][att_name] = _region_attachment(
                    att_name, att_data, ppu
                )
        result.skins[skin.name] = skin_out

    # --- animations ---
    for anim_name, anim in spine_file.animations.items():
        timelines = []

        for bone_name, bone_tl in anim.bones.items():
            bone_index = bone_index_by_name[bone_name]

            if bone_tl.rotate:
                timelines.append(
                    RotateTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.value, _parse_curve(kf.curve))
                            for kf in bone_tl.rotate
                        ],
                    )
                )
            if bone_tl.translate:
                timelines.append(
                    TranslateTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.x / ppu, kf.y / ppu, _parse_curve(kf.curve))
                            for kf in bone_tl.translate
                        ],
                    )
                )
            if bone_tl.scale:
                timelines.append(
                    ScaleTimeline(
                        bone_index=bone_index,
                        keyframes=[
                            (kf.time, kf.x, kf.y, _parse_curve(kf.curve))
                            for kf in bone_tl.scale
                        ],
                    )
                )

        for slot_name, slot_tl in anim.slots.items():
            slot_index = slot_index_by_name[slot_name]
            if slot_tl.attachment:
                timelines.append(
                    AttachmentTimeline(
                        slot_index=slot_index,
                        keyframes=[(kf.time, kf.name) for kf in slot_tl.attachment],
                    )
                )

        duration = max(
            (
                kf.time
                for tl_group in [anim.bones.values(), anim.slots.values()]
                for tl in tl_group
                for kfs in (
                    getattr(tl, "rotate", []),
                    getattr(tl, "translate", []),
                    getattr(tl, "scale", []),
                    getattr(tl, "attachment", []),
                )
                for kf in kfs
            ),
            default=0.0,
        )

        result.animations[anim_name] = Animation(anim_name, duration, timelines)

    return result
"""


def load_skeleton_data(path: str, ppu: float | None = None) -> SkeletonData:
    return convert(SpineSkeletonFile.load(path), ppu)
