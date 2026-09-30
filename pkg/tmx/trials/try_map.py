from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

tile_size = map.tile_size
print(tile_size.x)
print(tile_size.y)

tile_count = map.get_tile_count()
print(tile_count.x)
print(tile_count.y)