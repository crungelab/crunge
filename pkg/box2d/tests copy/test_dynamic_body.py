from crunge import box2d

# Create World
world_def = box2d.default_world_def()

print(world_def)

# worldDef.gravity = (b2Vec2){0.0f, -10.0f};
world_def.gravity = box2d.Vec2(0.0, -10.0)

world_id = box2d.create_world(world_def)

# Create Ground

# b2BodyDef groundBodyDef = b2DefaultBodyDef();
body_def = box2d.default_body_def()
print(body_def)

# groundBodyDef.position = (b2Vec2){0.0f, -10.0f};
body_def.position = box2d.Vec2(0.0, -10.0)
print(body_def.position)

# b2BodyId groundId = b2CreateBody(worldId, &groundBodyDef);
ground_id = box2d.create_body(world_id, body_def)

# b2Polygon groundBox = b2MakeBox(50.0f, 10.0f);
ground_box = box2d.make_box(50.0, 10.0)
print(ground_box)

# b2ShapeDef groundShapeDef = b2DefaultShapeDef();
shape_def = box2d.default_shape_def()
print(shape_def)
# b2CreatePolygonShape(groundId, &groundShapeDef, &groundBox);
box2d.create_polygon_shape(ground_id, shape_def, ground_box)

# Create Dynamic Body

#b2BodyDef bodyDef = b2DefaultBodyDef();
body_def = box2d.default_body_def()
print(body_def)

#bodyDef.type = b2_dynamicBody;
body_def.type = box2d.BodyType.DYNAMIC_BODY
#bodyDef.position = (b2Vec2){0.0f, 4.0f};
body_def.position = box2d.Vec2(0.0, 4.0)
#b2BodyId bodyId = b2CreateBody(worldId, &bodyDef);
body_id = box2d.create_body(world_id, body_def)

#b2Polygon dynamicBox = b2MakeBox(1.0f, 1.0f);
dynamic_box = box2d.make_box(1.0, 1.0)
print(dynamic_box)

#b2ShapeDef shapeDef = b2DefaultShapeDef();
shape_def = box2d.default_shape_def()
print(shape_def)
#shapeDef.density = 1.0f;
shape_def.density = 1.0
#shapeDef.material.friction = 0.3f;
shape_def.material.friction = 0.3

#b2CreatePolygonShape(bodyId, &shapeDef, &dynamicBox);
box2d.create_polygon_shape(body_id, shape_def, dynamic_box)
