from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

for layer in map.layers:
    if isinstance(layer, tmx.ObjectGroup):
        if layer.name != "pc":
            continue

        for object in layer.get_objects():
            print(object.name)
            print(object.get_class())
            print(object.properties)
            gid = object.get_tile_id()
            print(gid)
            tile = map.get_tile(gid)
            print(tile)
            print(tile.properties)
            print(tile.class_name)
