from crunge import box2d

world_def = box2d.default_world_def()

print(world_def)

#worldDef.gravity = (b2Vec2){0.0f, -10.0f};
world_def.gravity = box2d.Vec2(0.0, -10.0)

world_id = box2d.create_world(world_def)
