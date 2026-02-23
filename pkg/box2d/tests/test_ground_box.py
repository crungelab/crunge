from crunge import box2d

world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))

print(world_def)

world = box2d.create_world(world_def)

"""
#b2BodyDef groundBodyDef = b2DefaultBodyDef();
ground_body_def = box2d.default_body_def()
print(ground_body_def)

#groundBodyDef.position = (b2Vec2){0.0f, -10.0f};
ground_body_def.position = box2d.Vec2(0.0, -10.0)
print(ground_body_def.position)
"""

ground_body_def = box2d.BodyDef(position = box2d.Vec2(0.0, -10.0))
print(ground_body_def)

#b2BodyId groundId = b2CreateBody(worldId, &groundBodyDef);
#ground_id = box2d.create_body(world, ground_body_def)
ground_id = world.create_body(ground_body_def)

#b2Polygon groundBox = b2MakeBox(50.0f, 10.0f);
ground_box = box2d.make_box(50.0, 10.0)
print("Ground Box:")
print(ground_box)

#b2ShapeDef groundShapeDef = b2DefaultShapeDef();
#shape_def = box2d.default_shape_def()
shape_def = box2d.ShapeDef()
print("Shape Def:")
print(shape_def)
#b2CreatePolygonShape(groundId, &groundShapeDef, &groundBox);
box2d.create_polygon_shape(ground_id, shape_def, ground_box)
