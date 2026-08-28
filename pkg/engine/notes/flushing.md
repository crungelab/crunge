# Why vus defer GPU writes

## The short version

A chip's state arrives before the GPU resources that state gets written
into. Writing on assignment means writing into `None`. So assignment marks
dirt, and `flush()` does the write later, when the target exists.

If you are tempted to delete `flush()` and write directly from the setter,
read the rest of this first — that is what the code used to do, and every
failure below is one it actually produced.

## Why the state and the buffer arrive in different orders

There is no single order. Four different arrival orders are all legal:

1. **Model before buffer.** A sprite vu is appended to an instanced group,
   which assigns `node_buffer` _after_ `super().append()` returns. The vu
   was enabled before that, so `on_model_changed` already fired.

2. **Buffer before model.** A tile node is attached to a layer, then its
   model lands from a loader a frame later.

3. **Neither, then both.** A grouped vu (`manual_draw = False`) never
   creates buffers of its own at all — they come from the group, whenever
   the group gets around to it.

4. **Both, then the buffer is replaced.** A group re-indexes on removal, so
   `node_buffer_index` changes under a vu that was already written.

An eager write is correct for exactly one of those. Deferral is correct for
all four, because the write happens at a moment we control rather than at a
moment the caller happens to pick.

## Why not just guard the setter

`if self.is_enabled: self.update_gpu()` was the old guard, and it does not
work. `Base` sets the lifetime flag _before_ the hook fires, so by the time
`_enable` runs `sync()`, `is_enabled` is already true — but a grouped vu
still has no buffer. The guard passes and the write crashes.

Guarding on the buffer instead (`if self.node_buffer is not None`) turns the
crash into silence: the write is skipped and never retried, so the vu draws
with a stale or zeroed uniform forever. That was the tile-rendering bug —
sprites present, correctly positioned, invisible.

Deferral is the version that retries. `_flush_gpu` returns `False` when the
target is missing, the flag stays set, and the next frame tries again.

## Why writes cannot happen at draw time

`Renderer.render` opens the pass and then walks the tree:

    with self.render_pass():
        node.render()

`draw` therefore runs inside an open render pass, and buffer writes are not
legal there. `update` runs before the pass opens, which is why `flush` is
called from `update` and not from `draw`.

## Why the domains are separate

`Dirt` is a flag set, not a boolean, because the things that get rebuilt
have different targets and different readiness:

- `GEOMETRY` — vertex/index data. Needs a vertex buffer.
- `BINDING` — bind groups. Needs the buffers they reference to exist.
- `GPU` — uniform writes. Needs the uniform buffer.

They clear independently. A bind group that cannot be built because the
viewport has not been assigned should not force a geometry rebuild on the
retry, and vice versa. The flush order is geometry → binding → gpu, because
each feeds the next.

## Why `update` is not defined on the base

`Chip.__init_subclass__` decides bucket membership by looking for an
`update` override. If `Vu` defined `update`, every vu in the engine would
join `_updatables` whether it had anything to do or not. A vu with GPU state
opts in by defining `update` and calling `flush` from it.

## Chips outside the node walk

`flush` is driven by `update`, and `update` reaches a chip through the node
tree. Anything that owns GPU state but is _not_ reachable from that walk has
to drive its own flush. So far that is:

- `Lighting3D` — reached at `bind()` time from the renderer.
- `CameraChip` — same.
- vu groups — now chips on a layer root, so they are back on the walk.
- standalone vus in `deeper` — flushed by that project's own system loop.

Each of those is a `self.flush()` at the point of consumption. If a fourth
appears, that is the signal to make the thing a node rather than patch it
again.

## What breaks silently

Two failure modes here produce no traceback, so they are worth naming:

- **An orphaned handler.** `Vu3D.on_node_transform_change` survived a rename
  of the base class hook. Nothing called it, nothing raised, the transform
  stayed identity, and everything rendered collapsed at the origin. Renaming
  a signal handler needs a grep across the whole tree, not just the file.

- **A skipped rebuild.** `InstancedSpriteVuGroup.batch()` returning early on
  a missing sprite, with no rebuild scheduled, meant those vus never entered
  a batch and never drew. Any early return in a rebuild path needs a mark so
  it retries.
