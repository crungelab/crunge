from __future__ import annotations

import cv2
import numpy as np
from loguru import logger
import glm

from crunge import tmx

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder
from crunge.engine.d2.sprite import Sprite

from ...objects.tile import Tile, GhostTile, TerrainColliderTile


class BitmapTerrainBuilder(tiled_builder.DefaultTileLayerBuilder):
    """Builds terrain collision by compositing the collision hulls of every
    participating tile into one occupancy mask, tracing that mask once, and
    emitting chain shapes from the resulting contours.

    Replaces TileLayerRunBuilder. The run merger only removed seams between
    axis-aligned boxes on the same row; tracing at map scale removes them in
    every direction and works with arbitrary cv2-traced hulls.
    """

    # Tile classes that contribute geometry to the terrain mask. These become
    # GhostTile (visual only) since their collision now lives in the chains.
    TERRAIN_TILE_TYPES = {
        "terrain_stone_block_top",
        "terrain_stone_ramp_long_a",
        "terrain_stone_ramp_long_b",
        "terrain_stone_ramp_long_c",
    }

    # Morphological close radius in pixels. This is the "alpha" knob: it
    # bridges gaps between independently traced neighbouring hulls. Must stay
    # well below the narrowest gap the player needs to pass through.
    MASK_CLOSE_RADIUS = 2

    # approxPolyDP epsilon in pixels. Trades segment count against corner
    # fidelity - raise it if the broadphase shape count gets out of hand,
    # lower it if the skateboard clips corners.
    SIMPLIFY_EPSILON = 1.5

    # Contours smaller than this are specks from stray alpha.
    MIN_CONTOUR_AREA = 16.0

    # Drop enclosed cavities that no reachable empty space touches.
    DISCARD_SEALED_CAVITIES = True

    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            if properties.get("type") in self.TERRAIN_TILE_TYPES:
                return GhostTile(position, sprite)
            return Tile(position, sprite)

        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))

    # ------------------------------------------------------------------
    # Hooks - override these if the guessed accessors are wrong
    # ------------------------------------------------------------------

    def is_terrain_tile(self, tile) -> bool:
        return tile is not None and tile.class_name in self.TERRAIN_TILE_TYPES

    def get_sprite(self, tile_gid: int, flip_flags: int):
        """Fetch the sprite variant for this gid/flip combination.

        # ASSUMPTION: the (tile_gid, flip_flags) sprite cache on the base
        # builder. The variant matters because the collision points already
        # have the H/V/D transform baked in at build time - fetching the
        # unflipped variant would give hulls that disagree with the visuals.
        """
        return self.context.sprites.get((tile_gid, flip_flags))

    def get_hulls(self, sprite: Sprite) -> list[list[tuple[float, float]]]:
        """Tile-local collision polygons in TEXELS, CCW.

        # ASSUMPTION: property name. Returns either a single polygon or a
        # list of them; _normalize_hulls tolerates both.
        """
        return self._normalize_hulls(sprite.points)

    def get_flip_flags(self, tmx_tile) -> int:
        """Dense engine-side flip flags for a tmx layer cell.

        # ASSUMPTION: attribute name, and that the tmx->dense translation
        # helper lives on the builder. tmxlite uses non-dense bit values
        # (H=0x8, V=0x4, D=0x2); engine internals use H=1, V=2, D=4.
        """
        return self.translate_flip_flags(tmx_tile.flip_flags)

    # ------------------------------------------------------------------
    # Entry point - mirrors build_runs()'s signature
    # ------------------------------------------------------------------

    def build_terrain(self, tmx_layer: tmx.TileLayer):
        mask = self._build_mask(tmx_layer)
        if mask is None:
            logger.debug("TerrainBuilder: no terrain tiles in layer, skipping")
            return

        mask = self._bridge_seams(mask)

        reachable = self._exterior_mask(mask) if self.DISCARD_SEALED_CAVITIES else None

        paths = self._trace_paths(mask, reachable)
        if not paths:
            logger.warning("TerrainBuilder: mask produced no usable contours")
            return

        self._emit_collider(paths)

    # ------------------------------------------------------------------
    # 1. Hulls -> occupancy mask
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_hulls(hulls) -> list[list[tuple[float, float]]]:
        if not hulls:
            return []
        first = hulls[0]
        # A bare polygon looks like [(x, y), ...] - its first element is a
        # 2-scalar pair rather than another sequence of pairs.
        if len(first) == 2 and not hasattr(first[0], "__len__"):
            return [list(hulls)]
        return [list(h) for h in hulls]

    def _build_mask(self, tmx_layer: tmx.TileLayer) -> np.ndarray | None:
        map = self.map
        map_size = map.tile_count
        tile_size = map.tile_size
        tile_width = int(tile_size.x)
        tile_height = int(tile_size.y)
        tiles = tmx_layer.tiles

        mask = np.zeros(
            (map_size.y * tile_height, map_size.x * tile_width), dtype=np.uint8
        )

        filled = 0

        for j in range(map_size.y):
            for i in range(map_size.x):
                cell = tiles[j * map_size.x + i]
                tile_gid = cell.id
                if not tile_gid:
                    continue

                tile = map.get_tile(tile_gid)
                if not self.is_terrain_tile(tile):
                    continue

                sprite = self.get_sprite(tile_gid, self.get_flip_flags(cell))
                if sprite is None:
                    continue

                hulls = self.get_hulls(sprite)
                if not hulls:
                    # No traced hull: fall back to the full tile footprint so
                    # a solid tile never silently becomes a hole.
                    hulls = [
                        [
                            (0.0, 0.0),
                            (tile_width, 0.0),
                            (tile_width, tile_height),
                            (0.0, tile_height),
                        ]
                    ]

                ox = i * tile_width
                oy = j * tile_height

                ppu = self.ppu
                half_w = tile_width / 2
                half_h = tile_height / 2

                polys = [
                    np.array(
                        [(int(round(ox + half_w + hx * ppu)),
                        int(round(oy + half_h - hy * ppu)))
                        for hx, hy in hull],
                        dtype=np.int32,
                    )
                    for hull in hulls
                    if len(hull) >= 3
                ]

                '''
                polys = [
                    np.array(
                        [(int(round(ox + hx)), int(round(oy + hy))) for hx, hy in hull],
                        dtype=np.int32,
                    )
                    for hull in hulls
                    if len(hull) >= 3
                ]
                '''

                if polys:
                    cv2.fillPoly(mask, polys, 255)
                    filled += 1

        if filled == 0:
            return None

        logger.debug(
            f"TerrainBuilder: rasterized {filled} terrain tiles into "
            f"{mask.shape[1]}x{mask.shape[0]} mask"
        )
        return mask

    # ------------------------------------------------------------------
    # 2. Seam bridging
    # ------------------------------------------------------------------

    def _bridge_seams(self, mask: np.ndarray) -> np.ndarray:
        r = self.MASK_CLOSE_RADIUS
        if r <= 0:
            return mask
        k = 2 * r + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # ------------------------------------------------------------------
    # 3. Reachability
    # ------------------------------------------------------------------

    @staticmethod
    def _exterior_mask(mask: np.ndarray) -> np.ndarray:
        """True where empty AND reachable from outside the map."""
        h, w = mask.shape
        # Pad by one so terrain touching the map edge can still be flooded
        # around, then give floodFill the +2 scratch buffer it requires.
        padded = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
        scratch = np.zeros((h + 4, w + 4), np.uint8)
        cv2.floodFill(padded, scratch, (0, 0), 128)
        return padded[1:-1, 1:-1] == 128

    @staticmethod
    def _touches_reachable(reachable, cx: int, cy: int, r: int = 2) -> bool:
        h, w = reachable.shape
        y0, y1 = max(0, cy - r), min(h, cy + r + 1)
        x0, x1 = max(0, cx - r), min(w, cx + r + 1)
        return bool(reachable[y0:y1, x0:x1].any())

    # ------------------------------------------------------------------
    # 4. Trace -> world-space paths
    # ------------------------------------------------------------------

    def _to_world(self, px: float, py: float) -> tuple[float, float]:
        """Mask pixel space (Y-down) -> world units (Y-up).

        This reproduces the convention from build_runs():
            y = (j - 1) * tile_height + half_tile_height
            y = self.context.size.y - y
        i.e. a one-row upward shift before the flip. If the terrain lands one
        tile off vertically, this method is the only place to fix it.
        """
        tile_height = self.map.tile_size.y
        x = px 
        y = self.context.size.y - (py - tile_height)
        return (x / self.ppu, y / self.ppu)

    @staticmethod
    def _signed_area(poly) -> float:
        a = 0.0
        n = len(poly)
        for i in range(n):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n]
            a += x0 * y1 - x1 * y0
        return a * 0.5

    def _trace_paths(self, mask, reachable) -> list[tuple[list, bool]]:
        """Returns [(points_in_world_units, is_hole), ...]"""
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if hierarchy is None:
            return []
        hierarchy = hierarchy[0]

        paths: list[tuple[list, bool]] = []

        for idx, contour in enumerate(contours):
            if cv2.contourArea(contour) < self.MIN_CONTOUR_AREA:
                continue

            # A non-negative parent index means this contour bounds a hole
            # inside another contour rather than an outer silhouette.
            is_hole = hierarchy[idx][3] != -1

            if is_hole and reachable is not None:
                cx, cy = int(contour[0][0][0]), int(contour[0][0][1])
                if not self._touches_reachable(reachable, cx, cy):
                    continue

            approx = cv2.approxPolyDP(contour, self.SIMPLIFY_EPSILON, True)
            if len(approx) < 3:
                continue

            world = [self._to_world(float(p[0][0]), float(p[0][1])) for p in approx]

            # The Y flip inverts winding. Force outers CCW and holes CW so the
            # one-sided chain normals face empty space in both cases. If the
            # rider falls through floors but lands on ceilings, invert this.
            want_ccw = not is_hole
            if (self._signed_area(world) > 0.0) != want_ccw:
                world.reverse()

            paths.append((world, is_hole))

        logger.debug(
            f"TerrainBuilder: traced {len(paths)} paths, "
            f"{sum(len(p) for p, _ in paths)} total vertices"
        )
        return paths

    # ------------------------------------------------------------------
    # 5. Emit
    # ------------------------------------------------------------------

    def _emit_collider(self, paths: list[tuple[list, bool]]):
        """One static body carrying every terrain chain.

        # ASSUMPTION: TerrainColliderTile(paths) signature - guessing it takes
        # the path list and creates one b2Chain per entry with is_loop=True.
        # Note b2ChainDef.points is the deferred cxbind pointer-plus-count
        # field; that wrapper needs to land before this will run.
        """
        for path, is_hole in paths:
            collider = TerrainColliderTile(path)

            # Mirrors the RunColliderTile path: manual create() because this node
            # never went through create_node_cb.
            collider.create()  # TODO: still unclear why create() is manual here
            self.layer.attach(collider)

        logger.debug(f"TerrainBuilder: emitted collider with {len(paths)} chains")

    '''
    def _emit_collider(self, paths: list[tuple[list, bool]]):
        """One static body carrying every terrain chain.

        # ASSUMPTION: TerrainColliderTile(paths) signature - guessing it takes
        # the path list and creates one b2Chain per entry with is_loop=True.
        # Note b2ChainDef.points is the deferred cxbind pointer-plus-count
        # field; that wrapper needs to land before this will run.
        """
        collider = TerrainColliderTile(
            #[glm.vec2(x, y) for path, _ in paths for x, y in path][:0] or paths

        )

        # Mirrors the RunColliderTile path: manual create() because this node
        # never went through create_node_cb.
        collider.create()  # TODO: still unclear why create() is manual here
        self.layer.attach(collider)

        logger.debug(f"TerrainBuilder: emitted collider with {len(paths)} chains")
    '''
