from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

for layer in map.layers:
    #print(layer.get_name())
    print(layer.name)
    if isinstance(layer, tmx.TileLayer):
        print("is tile layer")
        for tile in layer.tiles:
            print(tile.id)
