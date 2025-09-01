from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

for tileset in map.tilesets:
    if tileset.name != "stickers":
        continue
    print(tileset.name)
    print(tileset.get_tile_count())
    #print(tileset.name)
    tiles = tileset.tiles

    for tile in tiles:
        print(tile.id)
        print(tile.image_path)
