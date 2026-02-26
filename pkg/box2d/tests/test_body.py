from crunge import box2d

class BodyData:
    def __init__(self, body):
        self.body = body

world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))

print("World Def:")
print(world_def)

#world = box2d.create_world(world_def)
world = box2d.World(world_def)

body_def = box2d.BodyDef(position = box2d.Vec2(0.0, -10.0))
print("Ground Body Def:")
print(body_def)

body = world.create_body(body_def)
print("Ground Body:")
print(body)

data = BodyData(body)
print("Body Data:")
print(data)
body.user_data = data
