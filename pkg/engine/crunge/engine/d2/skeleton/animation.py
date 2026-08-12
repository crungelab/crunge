# animation.py — timelines + playback

# animation.py (additions) — TranslateTimeline, ScaleTimeline, AttachmentTimeline
# Interpolation is linear-only for now; curve field is stored on each keyframe
# tuple and threaded through but ignored until bezier sampling lands (build
# order step 5).

from bisect import bisect_right

from .skeleton import Skeleton, Bone, Slot


def _bracket(keyframes, time):
    """Return (prev_kf, next_kf, t) where t in [0,1] is the lerp fraction
    between prev and next at `time`. keyframes is a list of tuples whose
    first element is always `time`. Clamps at both ends."""
    if len(keyframes) == 1:
        return keyframes[0], keyframes[0], 0.0

    times = [kf[0] for kf in keyframes]
    i = bisect_right(times, time)

    if i == 0:
        return keyframes[0], keyframes[0], 0.0
    if i >= len(keyframes):
        return keyframes[-1], keyframes[-1], 0.0

    prev_kf, next_kf = keyframes[i - 1], keyframes[i]
    span = next_kf[0] - prev_kf[0]
    t = 0.0 if span <= 0.0 else (time - prev_kf[0]) / span

    # curve is stored as the last element of prev_kf ("linear"/"stepped"/bezier tuple)
    if prev_kf[-1] == "stepped":
        t = 0.0

    return prev_kf, next_kf, t


class TranslateTimeline:
    def __init__(self, bone_index, keyframes):
        self.bone_index = bone_index
        self.keyframes = keyframes  # list of (time, x, y, curve)

    def apply(self, skeleton: Skeleton, time, weight):
        x, y = self._sample(time)
        bone = skeleton.bones[self.bone_index]
        d = bone.data
        target_x, target_y = d.x + x, d.y + y
        bone.x = bone.x + (target_x - bone.x) * weight if weight != 1.0 else target_x
        bone.y = bone.y + (target_y - bone.y) * weight if weight != 1.0 else target_y

    def _sample(self, time):
        prev_kf, next_kf, t = _bracket(self.keyframes, time)
        _, px, py, _ = prev_kf
        _, nx, ny, _ = next_kf
        return px + (nx - px) * t, py + (ny - py) * t


class ScaleTimeline:
    def __init__(self, bone_index, keyframes):
        self.bone_index = bone_index
        self.keyframes = keyframes  # list of (time, x, y, curve)

    def apply(self, skeleton: Skeleton, time, weight):
        sx, sy = self._sample(time)
        bone = skeleton.bones[self.bone_index]
        d = bone.data
        bone.scale_x = d.scale_x + (sx - d.scale_x) * weight if weight != 1.0 else sx
        bone.scale_y = d.scale_y + (sy - d.scale_y) * weight if weight != 1.0 else sy

    def _sample(self, time):
        prev_kf, next_kf, t = _bracket(self.keyframes, time)
        _, psx, psy, _ = prev_kf
        _, nsx, nsy, _ = next_kf
        return psx + (nsx - psx) * t, psy + (nsy - psy) * t


class AttachmentTimeline:
    """Discrete, not interpolated — a slot's attachment just switches at
    each keyframe's time. `name=None` means no attachment."""

    def __init__(self, slot_index, keyframes):
        self.slot_index = slot_index
        self.keyframes = keyframes  # list of (time, attachment_name)

    def apply(self, skeleton: Skeleton, time, weight):
        name = self._sample(time)
        slot = skeleton.slots[self.slot_index]
        skin = skeleton.data.skins.get(skeleton.current_skin_name, {})
        slot_attachments = skin.get(slot.data.name, {})
        slot.attachment = slot_attachments.get(name) if name else None

    def _sample(self, time):
        active = None
        for kf_time, kf_name in self.keyframes:
            if kf_time > time:
                break
            active = kf_name
        return active


class RotateTimeline:
    def __init__(self, bone_index, keyframes):
        self.bone_index = bone_index
        self.keyframes = keyframes  # list of (time, angle, curve)

    def apply(self, skeleton: Skeleton, time, weight):
        angle = self._sample(time)
        bone = skeleton.bones[self.bone_index]
        d = bone.data
        target = d.rotation + angle          # keyframe value is a delta from setup, always
        bone.rotation = bone.rotation + (target - bone.rotation) * weight if weight != 1.0 else target

    def _sample(self, time):
        prev_kf, next_kf, t = _bracket(self.keyframes, time)
        _, pa, _ = prev_kf
        _, na, _ = next_kf
        # Shortest-path angle interpolation — a keyframe pair like 170 -> -170
        # is a 20 degree turn, not 340. Without this, fast rotations snap
        # the wrong way around at the wrap boundary.
        diff = (na - pa + 180.0) % 360.0 - 180.0
        return pa + diff * t


class Animation:
    def __init__(self, name, duration, timelines):
        self.name = name
        self.duration = duration
        self.timelines: list[RotateTimeline] = (
            timelines  # + Translate/Scale/Deform/Attachment later
        )


class TrackEntry:
    def __init__(self, animation: "Animation", loop=True):
        self.animation = animation
        self.time = 0.0
        self.loop = loop


class AnimationState:
    def __init__(self, skeleton: "Skeleton"):
        self.skeleton = skeleton
        self.current: TrackEntry | None = None

    def set_animation(self, animation: "Animation", loop=True):
        self.current = TrackEntry(animation, loop)

    def update(self, delta):
        if not self.current:
            return
        self.current.time += delta
        if self.current.loop and self.current.animation.duration > 0:
            self.current.time %= self.current.animation.duration

    def apply(self):
        self.skeleton.set_to_setup_pose()
        if self.current:
            for tl in self.current.animation.timelines:
                tl.apply(self.skeleton, self.current.time, weight=1.0)
        self.skeleton.update_world_transforms()
