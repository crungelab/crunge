# animation.py — timelines + playback

# animation.py (additions) — TranslateTimeline, ScaleTimeline, AttachmentTimeline
# Interpolation is linear-only for now; curve field is stored on each keyframe
# tuple and threaded through but ignored until bezier sampling lands (build
# order step 5).

from bisect import bisect_right

from .skeleton import Skeleton, Bone, Slot

_NO_CHANGE = (
    object()
)  # sentinel distinct from a real "name=None" keyframe (explicit hide)


def _before_start(keyframes, time) -> bool:
    return time < keyframes[0][0]


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


class RotateTimeline:
    def __init__(self, bone_index, keyframes):
        self.bone_index = bone_index
        self.keyframes = keyframes  # list of (time, angle, curve)

    def apply(self, skeleton: Skeleton, time, weight):
        if _before_start(self.keyframes, time):
            return  # setup pose, already applied by set_to_setup_pose()

        angle = self._sample(time)
        bone = skeleton.bones[self.bone_index]
        d = bone.data
        target = d.rotation + angle  # keyframe value is a delta from setup, always
        bone.rotation = (
            bone.rotation + (target - bone.rotation) * weight
            if weight != 1.0
            else target
        )

    def _sample(self, time):
        prev_kf, next_kf, t = _bracket(self.keyframes, time)
        _, pa, _ = prev_kf
        _, na, _ = next_kf
        # Shortest-path angle interpolation — a keyframe pair like 170 -> -170
        # is a 20 degree turn, not 340. Without this, fast rotations snap
        # the wrong way around at the wrap boundary.
        diff = (na - pa + 180.0) % 360.0 - 180.0
        return pa + diff * t


class TranslateTimeline:
    def __init__(self, bone_index, keyframes):
        self.bone_index = bone_index
        self.keyframes = keyframes  # list of (time, x, y, curve)

    def apply(self, skeleton: Skeleton, time, weight):
        if _before_start(self.keyframes, time):
            return

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
        if _before_start(self.keyframes, time):
            return

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


class RGBATimeline:
    def __init__(self, slot_index, keyframes):
        self.slot_index = slot_index
        self.keyframes = keyframes  # (time, glm.vec4, curve)

    def apply(self, skeleton, time, weight):
        if _before_start(self.keyframes, time):
            return

        color = self._sample(time)
        slot = skeleton.slots[self.slot_index]
        slot.color = (
            slot.color + (color - slot.color) * weight if weight != 1.0 else color
        )

    def _sample(self, time):
        prev_kf, next_kf, t = _bracket(self.keyframes, time)
        return prev_kf[1] + (next_kf[1] - prev_kf[1]) * t


class AttachmentTimeline:
    def __init__(self, slot_index, keyframes):
        self.slot_index = slot_index
        self.keyframes = keyframes

    def apply(self, skeleton, time, weight):
        name = self._sample(time)
        if name is _NO_CHANGE:
            return  # before the first keyframe — leave the setup-pose attachment alone

        slot = skeleton.slots[self.slot_index]
        skin = skeleton.data.skins.get(skeleton.current_skin_name, {})
        default_skin = skeleton.data.skins.get("default", {})
        slot_attachments = skin.get(slot.data.name, {}) or default_skin.get(
            slot.data.name, {}
        )
        slot.attachment = slot_attachments.get(name) if name else None

    def _sample(self, time):
        active = _NO_CHANGE
        for kf_time, kf_name in self.keyframes:
            if kf_time > time:
                break
            active = kf_name
        return active


'''
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
'''


class SequenceTimeline:
    def __init__(self, slot_index, attachment, keyframes):
        self.slot_index = slot_index
        self.attachment = attachment
        self.keyframes = keyframes

    def apply(self, skeleton, time, weight):
        kf = self._active_keyframe(time)
        if kf is None:
            return

        index = kf.index
        if kf.delay > 0:
            index += int((time - kf.time) / kf.delay)

        count = self.attachment.sequence.count
        mode = kf.mode
        # ASSUMPTION: mode semantics inferred from names, not verified against
        # Spine's runtime. The dragon only uses "loop" and the default hold.
        if mode == "loop":
            index %= count
        elif mode == "pingpong":
            period = count * 2 - 2
            index %= period
            if index >= count:
                index = period - index
        else:
            index = min(index, count - 1)

        skeleton.slots[self.slot_index].sequence_index = index

    def _active_keyframe(self, time):
        active = None
        for kf in self.keyframes:
            if kf.time > time:
                break
            active = kf
        return active


class DrawOrderTimeline:
    def __init__(self, keyframes: list[tuple[float, list[tuple[str, int]]]]):
        self.keyframes = keyframes  # (time, [(slot_name, offset), ...])

    def apply(self, skeleton, time, weight):
        offsets = self._sample(time)
        if offsets is _NO_CHANGE:
            skeleton.draw_order = None  # None means "use setup order", set below
            return

        setup_order = list(range(len(skeleton.slots)))  # setup pose = data order
        if not offsets:
            skeleton.draw_order = setup_order
            return

        slot_index_by_name = {s.data.name: i for i, s in enumerate(skeleton.slots)}
        # Standard Spine algorithm: place offset slots at their target
        # positions first, then fill remaining slots into the gaps in order.
        order = [None] * len(setup_order)
        placed = set()
        for slot_name, offset in offsets:
            i = slot_index_by_name[slot_name]
            order[i + offset] = i
            placed.add(i)

        remaining = (i for i in setup_order if i not in placed)
        for pos in range(len(order)):
            if order[pos] is None:
                order[pos] = next(remaining)

        skeleton.draw_order = order

    def _sample(self, time):
        active = _NO_CHANGE
        for kf_time, offsets in self.keyframes:
            if kf_time > time:
                break
            active = offsets
        return active


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
