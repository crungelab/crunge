from __future__ import annotations

import numpy as np
from loguru import logger

from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import make_valid

from crunge import tmx

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder


class PolygonTerrainBuilder(tiled_builder.DefaultTileLayerBuilder):
    """Builds terrain collision by unioning the collision hulls of every
    participating tile into one polygonal region, then emitting one b2Chain
    per boundary ring.

    Vector replacement for the raster mask approach. Since sprite.points are
    already in world units, there is no PPU round trip and no pixel
    quantization - hull coordinates pass through to chain vertices unchanged
    apart from translation to tile position.
    """

    # Gap-bridging distance in WORLD UNITS (not pixels any more). The vector
    # analogue of the old morphological close: buffer out, then back in.
    # Must exceed the worst seam gap between independently traced neighbours
    # and stay well below the narrowest passage the rider must fit through.
    # At 64 PPU, 0.02 units == 1.28px. Set to 0.0 to disable.
    SEAM_BRIDGE = 0.02

    # Vertex simplification tolerance in world units. Replaces approxPolyDP.
    # 0.015 units == ~1px at 64 PPU.
    SIMPLIFY_TOLERANCE = 0.015

    # Drop specks and slivers, in square world units.
    MIN_POLYGON_AREA = 0.004

    # Interior rings smaller than this are discarded. In vector terms every
    # interior ring is by definition a fully enclosed cavity - a cave with a
    # mouth is a concavity in the exterior ring, not a hole - so this
    # subsumes the old flood-fill reachability test entirely.
    MIN_HOLE_AREA = 0.05

    def __init__(self, terrain_tile_types: set[str], create_node_cb=None, create_chunk_cb=None):
        self.TERRAIN_TILE_TYPES = terrain_tile_types
        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))
        self.create_chunk_cb = create_chunk_cb

    # ------------------------------------------------------------------
    # Hooks
    # ------------------------------------------------------------------

    def is_terrain_tile(self, tile) -> bool:
        return tile is not None and tile.class_name in self.TERRAIN_TILE_TYPES

    def get_sprite(self, tile_gid: int, flip_flags: int):
        return self.context.sprites.get((tile_gid, flip_flags))

    def get_hulls(self, sprite) -> list[list[tuple[float, float]]]:
        """Tile-local collision polygons, in WORLD UNITS, centre-relative,
        Y-up, CCW."""
        return self._normalize_hulls(getattr(sprite, "points", None))

    def get_flip_flags(self, tmx_tile) -> int:
        return self.translate_flip_flags(tmx_tile.flip_flags)

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def build_terrain(self, tmx_layer: tmx.TileLayer):
        polys = self._collect_polygons(tmx_layer)
        if not polys:
            logger.debug("TerrainBuilder: no terrain tiles in layer, skipping")
            return

        region = self._union(polys)
        if region is None or region.is_empty:
            logger.warning("TerrainBuilder: union produced empty region")
            return

        paths = self._extract_paths(region)
        if not paths:
            logger.warning("TerrainBuilder: region produced no usable rings")
            return

        self._emit_chunk(paths)

    # ------------------------------------------------------------------
    # 1. Hulls -> world-space shapely polygons
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_hulls(hulls) -> list[list[tuple[float, float]]]:
        """Tolerates a bare polygon, a list of polygons, or raw cv2 (N,1,2)."""
        if hulls is None:
            return []

        arr = np.asarray(hulls, dtype=object if isinstance(hulls, list) else None)

        # Raw cv2 contour shape (N, 1, 2) or a plain (N, 2) point array.
        if isinstance(hulls, np.ndarray):
            if hulls.ndim == 3 and hulls.shape[1] == 1:
                return [[(float(x), float(y)) for x, y in hulls.reshape(-1, 2)]]
            if hulls.ndim == 2 and hulls.shape[1] == 2:
                return [[(float(x), float(y)) for x, y in hulls]]

        if not len(hulls):
            return []

        first = hulls[0]
        # A bare polygon's first element is a 2-scalar pair.
        if len(first) == 2 and not hasattr(first[0], "__len__"):
            return [[(float(p[0]), float(p[1])) for p in hulls]]
        return [[(float(p[0]), float(p[1])) for p in h] for h in hulls]

    def _tile_centre(self, i: int, j: int) -> tuple[float, float]:
        """World-unit centre of cell (i, j). Mirrors build_runs():
            x = i * tile_width + half_tile_width
            y = (j - 1) * tile_height + half_tile_height
            y = context.size.y - y
        If terrain sits one row off vertically, this is the only place to fix.
        """
        tile_size = self.map.tile_size
        tw, th = float(tile_size.x), float(tile_size.y)

        x = i * tw + tw / 2
        y = (j - 1) * th + th / 2
        y = self.context.size.y - y
        return (x / self.ppu, y / self.ppu)

    def _collect_polygons(self, tmx_layer: tmx.TileLayer) -> list[Polygon]:
        map = self.map
        map_size = map.tile_count
        tiles = tmx_layer.tiles

        # Fallback footprint: one full cell, centre-relative, in units.
        tw_u = float(map.tile_size.x) / self.ppu
        th_u = float(map.tile_size.y) / self.ppu
        fallback = [
            (-tw_u / 2, -th_u / 2),
            (tw_u / 2, -th_u / 2),
            (tw_u / 2, th_u / 2),
            (-tw_u / 2, th_u / 2),
        ]

        polys: list[Polygon] = []
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

                hulls = self.get_hulls(sprite) or [fallback]

                cx, cy = self._tile_centre(i, j)

                for hull in hulls:
                    if len(hull) < 3:
                        continue
                    # Hulls are centre-relative and already Y-up in the same
                    # sense as world space, so this is a pure translation.
                    shell = [(cx + hx, cy + hy) for hx, hy in hull]
                    poly = Polygon(shell)
                    if not poly.is_valid:
                        # Self-intersecting traces (rare, but cv2 can emit
                        # them on thin features) become valid geometry here.
                        poly = make_valid(poly)
                    if poly.is_empty:
                        continue
                    polys.append(poly)

                filled += 1

        logger.debug(
            f"TerrainBuilder: collected {len(polys)} hull polygons "
            f"from {filled} terrain tiles"
        )
        return polys

    # ------------------------------------------------------------------
    # 2. Union + seam bridging
    # ------------------------------------------------------------------

    def _union(self, polys: list[Polygon]):
        """NOTE: unary_union, not coverage_union_all. The latter requires a
        valid coverage - non-overlapping polygons sharing exact vertices -
        which independently traced per-tile hulls do not form."""
        region = unary_union(polys)

        eps = self.SEAM_BRIDGE
        if eps > 0.0:
            # Vector morphological close. join_style=2 (mitre) keeps corners
            # sharp instead of rounding them off like the default.
            region = region.buffer(eps, join_style=2).buffer(-eps, join_style=2)

        return region

    # ------------------------------------------------------------------
    # 3. Region -> chain paths
    # ------------------------------------------------------------------

    def _extract_paths(self, region) -> list[tuple[list, bool]]:
        """Returns [(points, is_hole), ...] with exteriors CCW, holes CW."""
        if isinstance(region, Polygon):
            components = [region]
        elif isinstance(region, MultiPolygon):
            components = list(region.geoms)
        else:
            # GeometryCollection: keep only the polygonal parts.
            components = [g for g in getattr(region, "geoms", [])
                          if isinstance(g, Polygon)]

        paths: list[tuple[list, bool]] = []

        for poly in components:
            if poly.area < self.MIN_POLYGON_AREA:
                continue

            if self.SIMPLIFY_TOLERANCE > 0.0:
                poly = poly.simplify(self.SIMPLIFY_TOLERANCE,
                                     preserve_topology=True)
                if poly.is_empty or not isinstance(poly, Polygon):
                    continue

            # orient(sign=1.0) guarantees CCW exterior and CW interiors.
            # This replaces the signed-area guesswork - one-sided chain
            # normals now face empty space on both by construction.
            poly = orient(poly, sign=1.0)

            paths.append((self._ring_points(poly.exterior), False))

            for interior in poly.interiors:
                if Polygon(interior).area < self.MIN_HOLE_AREA:
                    continue
                paths.append((self._ring_points(interior), True))

        logger.debug(
            f"TerrainBuilder: extracted {len(paths)} rings, "
            f"{sum(len(p) for p, _ in paths)} total vertices"
        )
        return paths

    @staticmethod
    def _ring_points(ring) -> list[tuple[float, float]]:
        """Shapely rings repeat the first point at the end; b2Chain with
        is_loop=True closes itself, so drop the duplicate."""
        coords = list(ring.coords)
        if len(coords) > 1 and coords[0] == coords[-1]:
            coords = coords[:-1]
        return [(float(x), float(y)) for x, y in coords]

    # ------------------------------------------------------------------
    # 4. Emit
    # ------------------------------------------------------------------

    def _emit_chunk(self, paths: list[tuple[list, bool]]):
        for path, is_hole in paths:
            chunk = self.create_chunk_cb(path)
            chunk.create()
            self.layer.attach(chunk)

        logger.debug(f"TerrainBuilder: emitted {len(paths)} chains")