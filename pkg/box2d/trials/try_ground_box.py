from crunge import box2d

world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))

print("World Def:")
print(world_def)

#world = box2d.create_world(world_def)
world = box2d.World(world_def)

ground_body_def = box2d.BodyDef(position = box2d.Vec2(0.0, -10.0))
print("Ground Body Def:")
print(ground_body_def)

ground_body = world.create_body(ground_body_def)
print("Ground Body:")
print(ground_body)

ground_box = box2d.make_box(50.0, 10.0)
print("Ground Box:")
print(ground_box)

ground_shape_def = box2d.ShapeDef()
print("Ground Shape Def:")
print(ground_shape_def)

ground_shape = ground_body.create_polygon_shape(ground_shape_def, ground_box)
print("Ground Shape:")
print(ground_shape)
