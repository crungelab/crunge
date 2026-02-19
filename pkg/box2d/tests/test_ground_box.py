from crunge import box2d

world_def = box2d.default_world_def()

print(world_def)

#worldDef.gravity = (b2Vec2){0.0f, -10.0f};
world_def.gravity = box2d.Vec2(0.0, -10.0)

world_id = box2d.create_world(world_def)

#b2BodyDef groundBodyDef = b2DefaultBodyDef();
body_def = box2d.default_body_def()
print(body_def)

#groundBodyDef.position = (b2Vec2){0.0f, -10.0f};
body_def.position = box2d.Vec2(0.0, -10.0)
print(body_def.position)

#b2BodyId groundId = b2CreateBody(worldId, &groundBodyDef);
ground_id = box2d.create_body(world_id, body_def)

#b2Polygon groundBox = b2MakeBox(50.0f, 10.0f);
ground_box = box2d.make_box(50.0, 10.0)
print(ground_box)

#b2ShapeDef groundShapeDef = b2DefaultShapeDef();
shape_def = box2d.default_shape_def()
print(shape_def)
#b2CreatePolygonShape(groundId, &groundShapeDef, &groundBox);
box2d.create_polygon_shape(ground_id, shape_def, ground_box)
