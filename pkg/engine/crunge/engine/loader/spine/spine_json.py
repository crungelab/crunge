# spine_json.py — Pydantic models mirroring Spine's JSON export schema
# Ref: http://esotericsoftware.com/spine-json-format

from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class SpineBaseModel(BaseModel):
    # Spine's JSON is camelCase; keep our attrs snake_case internally later,
    # but at the loader boundary just consume camelCase directly via alias.
    # model_config = ConfigDict(populate_by_name=True, extra="allow")
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


# ---------- skeleton metadata ----------


class SkeletonMeta(SpineBaseModel):
    hash: str | None = None
    spine: str | None = None  # exporter version string, e.g. "4.2.43"
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    fps: float = 30.0
    images: str | None = None
    audio: str | None = None


# ---------- bones ----------


class BoneJSON(SpineBaseModel):
    name: str
    parent: str | None = None
    length: float = 0.0
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scaleX: float = 1.0
    scaleY: float = 1.0
    shearX: float = 0.0
    shearY: float = 0.0

    inherit: Literal[  # TODO
        "normal",
        "onlyTranslation",
        "noRotationOrReflection",
        "noScale",
        "noScaleOrReflection",
    ] = "normal"

    color: str | None = None  # nonessential, ignore for now


# ---------- slots ----------


class SlotJSON(SpineBaseModel):
    name: str
    bone: str
    color: str = "FFFFFFFF"
    attachment: str | None = None
    blend: Literal["normal", "additive", "multiply", "screen"] = "normal"


# ---------- sequences (optional) ----------


class SequenceJSON(SpineBaseModel):
    count: int = 0
    start: int = 1
    digits: int = 0
    setupIndex: int = 0


class SequenceKeyframe(SpineBaseModel):
    time: float = 0.0
    mode: str = "hold"
    index: int = 0
    delay: float = 0.0


# ---------- attachments (region only for now; mesh/etc pass through) ----------

# spine_json.py — add to RegionAttachmentJSON


class RegionAttachmentJSON(SpineBaseModel):
    type: Literal["region"] = "region"
    name: str | None = None
    path: str | None = None
    x: float = 0.0
    y: float = 0.0
    scaleX: float = 1.0
    scaleY: float = 1.0
    rotation: float = 0.0
    width: float = 0.0
    height: float = 0.0
    color: str = "FFFFFFFF"
    sequence: SequenceJSON | None = None


# Skins are keyed: skin_name -> slot_name -> attachment_name -> attachment dict.
# We don't know `type` until we look at the dict, so keep it raw here and
# dispatch in the loader (region now, mesh/linkedmesh/etc later).
SkinAttachments = dict[str, dict[str, dict]]


class SkinJSON(SpineBaseModel):
    name: str
    bones: list[str] = Field(
        default_factory=list
    )  # ASSUMPTION: unused until skin-scoped bones needed
    ik: list[str] = Field(default_factory=list)
    transform: list[str] = Field(default_factory=list)
    path: list[str] = Field(default_factory=list)
    attachments: SkinAttachments = Field(default_factory=dict)


# ---------- draw order ----------
# spine_json.py


class DrawOrderOffsetJSON(SpineBaseModel):
    slot: str
    offset: int = 0


class DrawOrderKeyframe(SpineBaseModel):
    time: float = 0.0
    offsets: list[DrawOrderOffsetJSON] = Field(default_factory=list)


# ---------- animation keyframes ----------


class RotateKeyframe(SpineBaseModel):
    time: float = 0.0
    value: float = 0.0
    curve: float | str | list[float] | None = (
        None  # None=linear, "stepped", or [cx1,cy1,cx2,cy2]
    )


class TranslateKeyframe(SpineBaseModel):
    time: float = 0.0
    x: float = 0.0
    y: float = 0.0
    curve: float | str | list[float] | None = None


class ScaleKeyframe(SpineBaseModel):
    time: float = 0.0
    x: float = 1.0
    y: float = 1.0
    curve: float | str | list[float] | None = None


class AttachmentKeyframe(SpineBaseModel):
    time: float = 0.0
    name: str | None = None  # None = no attachment at this keyframe


class BoneTimelinesJSON(SpineBaseModel):
    rotate: list[RotateKeyframe] = Field(default_factory=list)
    translate: list[TranslateKeyframe] = Field(default_factory=list)
    scale: list[ScaleKeyframe] = Field(default_factory=list)
    shear: list[dict] = Field(
        default_factory=list
    )  # TODO: ShearKeyframe when we need it


class SlotTimelinesJSON(SpineBaseModel):
    attachment: list[AttachmentKeyframe] = Field(default_factory=list)
    rgba: list[dict] = Field(default_factory=list)  # color timeline, TODO
    # sequence: list[SequenceKeyframe] = Field(default_factory=list)


class AttachmentTimelinesJSON(SpineBaseModel):
    """Timelines nested under an animation's `attachments` key, shaped
    slot_name -> attachment_name -> { timeline_type: [keyframes] }."""

    sequence: list[SequenceKeyframe] = Field(default_factory=list)
    deform: list[dict] = Field(default_factory=list)  # TODO


class AnimationJSON(SpineBaseModel):
    bones: dict[str, BoneTimelinesJSON] = Field(default_factory=dict)
    slots: dict[str, SlotTimelinesJSON] = Field(default_factory=dict)
    # skin_name -> slot_name -> attachment_name -> timelines
    attachments: dict[str, dict[str, dict[str, AttachmentTimelinesJSON]]] = Field(
        default_factory=dict
    )
    ik: dict[str, list[dict]] = Field(default_factory=dict)
    deform: dict = Field(default_factory=dict)
    events: list[dict] = Field(default_factory=list)
    draw_order: list[DrawOrderKeyframe] = Field(default_factory=list, alias="drawOrder")


# ---------- top-level file ----------


class SpineSkeletonFile(SpineBaseModel):
    skeleton: SkeletonMeta = Field(default_factory=SkeletonMeta)
    bones: list[BoneJSON] = Field(default_factory=list)
    slots: list[SlotJSON] = Field(default_factory=list)
    ik: list[dict] = Field(default_factory=list)  # TODO
    transform: list[dict] = Field(default_factory=list)  # TODO
    path: list[dict] = Field(default_factory=list)  # TODO
    skins: list[SkinJSON] = Field(default_factory=list)
    events: dict[str, dict] = Field(default_factory=dict)  # TODO
    animations: dict[str, AnimationJSON] = Field(default_factory=dict)

    @classmethod
    def load(cls, path: str) -> "SpineSkeletonFile":
        import json

        with open(path) as f:
            return cls.model_validate(json.load(f))
