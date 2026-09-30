from crunge.box2d import SurfaceMaterial
from crunge.box2d import ShapeDef

m = SurfaceMaterial()
print(m.friction, m.restitution, m.rolling_resistance,
      m.tangent_speed, m.user_material_id, m.custom_color)

sd = ShapeDef()
sd.material.friction = 0.123
print(sd.material.friction)

shape_def = ShapeDef()
m = shape_def.material
m.friction = 0.123
print(shape_def.material.friction)
