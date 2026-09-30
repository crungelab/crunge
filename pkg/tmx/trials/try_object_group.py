from pathlib import Path

from crunge import tmx

maps_root = Path(__file__).parent.parent.parent.parent / "resources" / "tiled"

path = maps_root / "level1.tmx"

map = tmx.Map()
map.load(str(path))

for layer in map.layers:
    #print(layer.get_name())
    print(layer.name)
    if isinstance(layer, tmx.ObjectGroup):
        print("is object group")
        print(layer.properties)

        for object in layer.get_objects():
            print(object.properties)
            gid = object.get_tile_id()
            print(gid)
            tile = map.get_tile(gid)
            print(tile)
