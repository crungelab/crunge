from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

for tileset in map.tilesets:
    print(tileset.get_name())
    #print(tileset.name)
    tiles = tileset.get_tiles()
    for tile in tiles:
        print(tile.id)
        print(tile.image_path)
