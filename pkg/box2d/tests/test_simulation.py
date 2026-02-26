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


# Create Dynamic Body

dynamic_body_def = box2d.BodyDef(type = box2d.BodyType.DYNAMIC_BODY, position = box2d.Vec2(0.0, 4.0))
print("Dynamic Body Def:")
print(dynamic_body_def)

dynamic_body = world.create_body(dynamic_body_def)
print("Dynamic Body:")
print(dynamic_body)

dynamic_box = box2d.make_box(1.0, 1.0)
print("Dynamic Box:")
print(dynamic_box)

dynamic_shape_def = box2d.ShapeDef(density = 1.0, material = box2d.SurfaceMaterial(friction = 0.3))
print("Dynamic Shape Def:")
print(dynamic_shape_def)

dynamic_shape = dynamic_body.create_polygon_shape(dynamic_shape_def, dynamic_box)
print("Dynamic Shape:")
print(dynamic_shape)

#float timeStep = 1.0f / 60.0f;
time_step = 1.0 / 60.0

#int subStepCount = 4;
sub_step_count = 4

"""
for (int i = 0; i < 90; ++i)
{
    b2World_Step(worldId, timeStep, subStepCount);
    b2Vec2 position = b2Body_GetPosition(bodyId);
    b2Rot rotation = b2Body_GetRotation(bodyId);
    printf("%4.2f %4.2f %4.2f\n", position.x, position.y, b2Rot_GetAngle(rotation));
}
"""

for i in range(90):
    world.step(time_step, sub_step_count)
    position = dynamic_body.get_position()
    rotation = dynamic_body.get_rotation()
    angle = rotation.get_angle()
    print(f"{position.x:.2f} {position.y:.2f} {angle:.2f}")

world.destroy()

"""
for i in range(90):
    box2d.world_step(world, time_step, sub_step_count)
    position = box2d.body_get_position(dynamic_body)
    rotation = box2d.body_get_rotation(dynamic_body)
    angle = box2d.rot_get_angle(rotation)
    print(f"{position.x:.2f} {position.y:.2f} {angle:.2f}")

#b2DestroyWorld(worldId);
box2d.destroy_world(world)
"""