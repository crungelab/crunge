from loguru import logger

from ...render_state import RenderState
from ...vu_group import Run, ELEMENTS
from ..vu_group_2d import VuGroup2D

from .sprite_vu import SpriteVu
from .sprite_group import SpriteGroup


class SpriteRun(Run):
    """A run of sprites sharing one texture.

    Carries a representative vu rather than just the texture, because the
    material bind group is reached through the sprite.
    """

    __slots__ = ("vu", "texture")

    def __init__(self, vu: SpriteVu, first: int) -> None:
        super().__init__(first)
        self.vu = vu
        self.texture = vu.sprite.texture


class SpriteVuGroup(VuGroup2D[SpriteVu]):
    """Sprite binding unit.

    Replaces the BaseSpriteVuGroup / SpriteVuGroup / DynamicSpriteVuGroup /
    InstancedSpriteVuGroup ladder. That ladder baked the draw strategy into
    the type hierarchy; instancing is now an emission decision, expressed by
    what new_run/extends/draw_run do, so a non-instanced or depth-tested
    variant is a sibling of this class rather than another rung.

    `program` is required and injected, never defaulted. Reaching for
    InstancedSpriteProgram here would make this module depend on the
    `instanced` subpackage it sits above, and importing anything from that
    package runs its __init__ — which is how an earlier import cycle formed.
    """

    def __init__(
        self,
        count: int = ELEMENTS,
        sprite_group: SpriteGroup = None,
        program=None,
        sort_by_material: bool = False,
    ) -> None:
        if program is None or callable(program):
            raise TypeError(
                f"{type(self).__name__} needs a program instance, got "
                f"{program!r} — e.g. InstancedSpriteProgram(), not the class"
            )
        super().__init__(count, program)
        self.sprite_group = sprite_group
        self.sort_by_material = sort_by_material

    @property
    def key(self) -> type:
        return SpriteVu

    # -- planning ----------------------------------------------------------

    def ready(self, vu: SpriteVu) -> bool:
        return vu.sprite is not None

    def sort_key(self, vu: SpriteVu):
        """Depth, then append order — material only when asked for.

        Material must NOT be in the default key. A layer whose vus all sit
        at depth 0, which is every layer that establishes order by the order
        it appends, would then sort entirely by texture: the append order is
        discarded and overlapping sprites draw in the wrong order. That is a
        visible rendering bug, not a slow frame, so the default declines the
        batching and keeps the ordering.

        With material out, this reproduces the old adjacent-only merging
        exactly: the stable sort carries append order through untouched, and
        extends() forms runs only where equal textures already sit next to
        each other.
        """
        if not self.sort_by_material:
            return (vu.sort_key, vu.group_sequence)

        # Opt-in. Only safe when same-depth sprites don't overlap — the
        # reorder happens strictly inside a depth tie, so it is correct
        # exactly when a tie means "order between these doesn't matter".
        #
        # TODO: id() groups stably but orders arbitrarily among materials. A
        # registered material index would make the plan reproducible across
        # runs, which matters the day you diff it.
        return (vu.sort_key, id(vu.sprite.texture), vu.group_sequence)

    def new_run(self, vu: SpriteVu, first: int) -> SpriteRun:
        return SpriteRun(vu, first)

    def extends(self, run: SpriteRun, vu: SpriteVu) -> bool:
        # Independent of sort_by_material: merging adjacent equal textures
        # never reorders anything, so it is always safe. The flag only
        # decides whether the sort goes looking for more adjacency.
        #
        # TODO: compare materials once they are registered.
        return run.texture is vu.sprite.texture

    # -- drawing -----------------------------------------------------------

    def draw_run(self, state: RenderState, run: SpriteRun) -> None:
        """Three bind groups, each at the index it carries itself.

        No slot numbers here. Each of these lands at BindGroupIndex.MODEL,
        .NODE and .MATERIAL respectively, and RenderState reads that off
        the object rather than taking one from this call site — so two of
        them writing the same index is a collision the cache can see, not a
        silent overwrite.

        The order is arbitrary. Every one of these is a no-op when the
        previous run already left it live, which for a run of sprites from
        one group means only the material actually changes.
        """
        state.set_pipeline(self.program)
        # Reaches past sprite_group.bind() into the bind group itself,
        # because the cache needs the object, not the side effect. Passing a
        # RenderState into BaseSpriteGroup.bind would be tidier and changes
        # every group's signature plus the self-drawing callers.
        state.set_bind_group(self.sprite_group.bind_group)
        state.set_bind_group(self.node_bind_group)
        # Material only. A sprite's own bind() also binds its membership's
        # ModelBindGroup, which would overwrite the dynamic group's at the
        # same index and stop matching the pipeline layout.
        state.set_bind_group(run.vu.sprite.material_bind_group)

        state.pass_enc.draw(4, run.count, 0, run.first)