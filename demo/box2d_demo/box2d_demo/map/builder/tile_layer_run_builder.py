from loguru import logger
import glm

from crunge import tmx

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder

from ...objects.tile import Tile, GhostTile, RunColliderTile

class TileLayerRunBuilder(tiled_builder.DefaultTileLayerBuilder):

    RUN_TILE_TYPE = "terrain_stone_block_right"

    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            if properties.get("type") == self.RUN_TILE_TYPE:
                return GhostTile(position, sprite)
            return Tile(position, sprite)

        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))

    def build_runs(self, tmx_layer: tmx.TileLayer):
        map = self.map
        map_size = map.tile_count
        tile_size = map.tile_size
        tile_width = tile_size.x
        tile_height = tile_size.y
        half_tile_width = tile_width / 2
        half_tile_height = tile_height / 2
        tiles = tmx_layer.tiles

        for j in range(map_size.y):
            run_start_i = None

            for i in range(map_size.x):
                tile_gid = tiles[j * map_size.x + i].id
                tile = map.get_tile(tile_gid)

                is_run_tile = (
                    tile is not None
                    and tile.class_name == self.RUN_TILE_TYPE
                )

                if is_run_tile:
                    if run_start_i is None:
                        run_start_i = i
                    continue

                # Non-run tile (or empty cell) closes out any open run.
                if run_start_i is not None:
                    self._emit_run_collider(
                        j, run_start_i, i - 1,
                        tile_width, tile_height, half_tile_height,
                    )
                    run_start_i = None

                if tile is None:
                    continue

                x = i * tile_width + half_tile_width
                y = (j - 1) * tile_height + half_tile_height
                y = self.context.size.y - y

                position = glm.vec2(x, y) / self.ppu

                # ... whatever non-run per-tile handling you already had here.
                # GhostTile/Tile themselves were already created by
                # create_node_cb inside super().build() above - this second
                # pass only needs to exist for the run-merging below.

            # Row ended mid-run (run touches the right edge of the map).
            if run_start_i is not None:
                self._emit_run_collider(
                    j, run_start_i, map_size.x - 1,
                    tile_width, tile_height, half_tile_height,
                )

    def _emit_run_collider(self, j, start_i, end_i, tile_width, tile_height, half_tile_height):
        """Create one merged static collider spanning tiles [start_i, end_i]
        on row j - replaces what would otherwise be (end_i - start_i + 1)
        separate per-tile boxes, eliminating the internal seams that were
        snagging the wheels."""
        run_tile_count = end_i - start_i + 1
        width = run_tile_count * tile_width

        center_x = start_i * tile_width + width / 2
        y = (j - 1) * tile_height + half_tile_height
        y = self.context.size.y - y

        position = glm.vec2(center_x, y) / self.ppu
        size = glm.vec2(width, tile_height) / self.ppu

        box_tile = RunColliderTile(position, size)
        box_tile.create() # TODO: Why am I having to manually call create() here?
        logger.debug(f"Emitted run collider: start_i={start_i}, end_i={end_i}, j={j}, position={position}, size={size}")

        self.layer.attach(box_tile)
