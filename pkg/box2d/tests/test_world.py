from crunge import box2d

world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))

print(world_def)
print(world_def.gravity)

world = box2d.create_world(world_def)

print(world)