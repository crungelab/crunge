from loguru import logger
import glm

import crunge.box2d as box2d

from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from crunge.engine.d2.sprite import SpriteVu
from ...entity import PhysicsGroup2D, Entity2D, DynamicEntity2D
from ...physics import BoxGeom, BallGeom
from ...physics import globe as physics_globe

from ...util import debounce

from .skateboard_controller import SkateboardController

# WHEEL_RADIUS = 0.3
WHEEL_RADIUS = 0.25
WHEEL_MASS = 2

CHASSIS_WIDTH = 0.5
CHASSIS_HEIGHT = 0.1
CHASSIS_MASS = 40

X_PAD = 0.3
Y_PAD = 0.25
# Y_PAD = WHEEL_RADIUS

# SPEED_DELTA = 1.0
SPEED_DELTA = 0.5
# MAX_SPEED = 100.0
# MAX_SPEED = 200.0
# MAX_SPEED = 8000.0
MAX_SPEED = 16000.0

# Box2D v3's revolute joint has a built-in motor, so there's no separate
# "max_force" concept for the joint itself - this becomes max_motor_torque.
# MAX_MOTOR_TORQUE = 4000.0
# MAX_MOTOR_TORQUE = 16000.0
MAX_MOTOR_TORQUE = 16000.0
# MAX_MOTOR_TORQUE = 20.0
# MAX_MOTOR_TORQUE = 100.0
# MAX_MOTOR_TORQUE = 500.0
# MAX_MOTOR_TORQUE = 1000.0

sprite_loader = SpriteLoader(sprite_builder=CollidableSpriteBuilder())


class Wheel(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load(":resources:/tiled/items/coinGold.png")
        # scale = glm.vec2(0.5, 0.5)
        scale = glm.vec2(WHEEL_RADIUS * 2, WHEEL_RADIUS * 2)
        super().__init__(
            position, scale=scale, vu=SpriteVu(), model=sprite, geom=BallGeom()
        )
        self.mass = WHEEL_MASS

    def add_shape(self, shape):
        # shape.set_density(WHEEL_MASS / (4/3 * 3.14159 * WHEEL_RADIUS**3), True)
        shape.set_density(0.01, True)
        pass

    @classmethod
    def produce(self, position=glm.vec2()):
        return Wheel(position)


class Chassis(DynamicEntity2D):
    def __init__(self, position=glm.vec2()):
        sprite = sprite_loader.load(":resources:/tiled/objects/boxCrate.png")

        scale = glm.vec2(1.5, 0.1)
        super().__init__(
            position, scale=scale, vu=SpriteVu(), model=sprite, geom=BoxGeom()
        )
        self.mass = CHASSIS_MASS

    def add_shape(self, shape):
        # shape.set_density(CHASSIS_MASS / (CHASSIS_WIDTH * CHASSIS_HEIGHT), True)
        shape.set_density(0.5, True)

    @classmethod
    def produce(self, position=glm.vec2()):
        return Chassis(position)


class Skateboard(PhysicsGroup2D):
    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.mountee = None
        self.mountee_joints = []
        self.speed = 0
        self.motors_attached = True

        chassis_pos = position
        front_wheel_pos = chassis_pos - glm.vec2(-(CHASSIS_WIDTH / 2 + X_PAD), Y_PAD)
        back_wheel_pos = chassis_pos - glm.vec2(CHASSIS_WIDTH / 2 + X_PAD, Y_PAD)

        # Kept for building the wheel joints' chassis-local anchors in _create,
        # since Box2D wants a single precise anchor rather than pymunk's
        # two-pin approximation (see _create below).
        self._front_wheel_pos = front_wheel_pos
        self._back_wheel_pos = back_wheel_pos

        self.chassis = chassis = self.add_node(Chassis.produce(chassis_pos))
        self.vu = chassis.vu
        self.front_wheel = self.add_node(Wheel.produce(front_wheel_pos))
        self.back_wheel = self.add_node(Wheel.produce(back_wheel_pos))

    @property
    def velocity(self):
        return self.chassis.velocity

    @classmethod
    def produce(self, position=glm.vec2(0, 0)):
        return Skateboard(position)

    def control(self):
        return SkateboardController(self)

    def mount(self, mountee: Entity2D):
        self.mountee = mountee
        point = glm.vec2(0, 0.6)
        mountee.on_mount(self.chassis, point)
        logger.debug(f"mountee body: {mountee.body}")

        world = physics_globe.physics_engine  # ASSUMPTION

        # pymunk used two PinJoints sharing the same anchor on both bodies as
        # a "weld" trick (fixes relative position AND rotation between the
        # two bodies). Box2D v3 has a real weld joint, so this collapses to
        # one joint instead of two.
        mountee_anchor = box2d.Vec2(0, -0.3)
        mounted_anchor = box2d.Vec2(0, 0.3)
        weld_def = box2d.WeldJointDef(
            body_id_a=self.chassis.body,
            body_id_b=mountee.body,
            local_frame_a=box2d.Transform(p=mounted_anchor),
            local_frame_b=box2d.Transform(p=mountee_anchor),
            # Angular is the one that matters here since it's rotational wobble.
            # angular_hertz=3.0,          # ASSUMPTION field name — low = soft/absorbing
            # angular_damping_ratio=1.0,  # ASSUMPTION field name — <1 = some give, >1 = overdamped
            # linear_hertz=0.0,           # 0 = keep linear fully rigid (rider shouldn't slide on board)
            # linear_damping_ratio=0.0,
        )
        weld_joint = box2d.create_weld_joint(world, weld_def)  # ASSUMPTION
        self.mountee_joints = [weld_joint]

    def dismount(self):
        logger.debug("dismounting")
        if self.mountee is None:
            return
        world = physics_globe.physics_engine
        for joint_id in self.mountee_joints:
            box2d.destroy_joint(joint_id, False)  # ASSUMPTION
        self.mountee_joints = []
        point = glm.vec2(0, CHASSIS_HEIGHT / 2)
        self.mountee.on_dismount(self.chassis, point)
        self.mountee = None

    def _create(self):
        super()._create()

        world = physics_globe.physics_engine

        # Each wheel gets a single revolute joint pinned at the wheel's
        # center, anchored on the chassis at the wheel's actual chassis-local
        # position. This replaces pymunk's two-PinJoint approximation with an
        # exact pivot, and folds the separate SimpleMotor into the joint's
        # built-in motor.
        front_anchor_on_chassis = box2d.Vec2(  # ASSUMPTION
            *(self._front_wheel_pos - self.chassis.position)
        )
        back_anchor_on_chassis = box2d.Vec2(  # ASSUMPTION
            *(self._back_wheel_pos - self.chassis.position)
        )
        wheel_anchor = box2d.Vec2(0, 0)  # ASSUMPTION

        front_joint_def = box2d.RevoluteJointDef(
            body_id_a=self.front_wheel.body,
            body_id_b=self.chassis.body,
            local_frame_a=box2d.Transform(p=wheel_anchor),
            local_frame_b=box2d.Transform(p=front_anchor_on_chassis),
            enable_motor=True,
            motor_speed=self.speed,
            max_motor_torque=MAX_MOTOR_TORQUE,
            #damping_ratio=1.0,
        )

        back_joint_def = box2d.RevoluteJointDef(
            body_id_a=self.back_wheel.body,
            body_id_b=self.chassis.body,
            local_frame_a=box2d.Transform(p=wheel_anchor),
            local_frame_b=box2d.Transform(p=back_anchor_on_chassis),
            enable_motor=True,
            motor_speed=self.speed,
            max_motor_torque=MAX_MOTOR_TORQUE,
            #damping_ratio=1.0,
        )

        self.front_joint = box2d.create_revolute_joint(  # ASSUMPTION
            world, front_joint_def
        )
        self.back_joint = box2d.create_revolute_joint(  # ASSUMPTION
            world, back_joint_def
        )

        # Kept as aliases so accelerate/decelerate/coast below read the same
        # as the old motor-based code even though there's no separate motor
        # object anymore - the "motor" now lives on the joint itself.
        self.front_motor = self.front_joint
        self.back_motor = self.motor = self.back_joint

    def attach_motors(self):
        if self.motors_attached:
            return
        box2d.revolute_joint_enable_motor(self.front_joint, True)  # ASSUMPTION
        box2d.revolute_joint_enable_motor(self.back_joint, True)  # ASSUMPTION
        box2d.revolute_joint_set_motor_speed(self.front_joint, self.speed)  # ASSUMPTION
        box2d.revolute_joint_set_motor_speed(self.back_joint, self.speed)  # ASSUMPTION
        self.motors_attached = True

    def detach_motors(self):
        if not self.motors_attached:
            return
        box2d.revolute_joint_enable_motor(self.front_joint, False)
        box2d.revolute_joint_enable_motor(self.back_joint, False)
        self.motors_attached = False

    def accelerate(self, rate=SPEED_DELTA):
        speed = self.speed + rate
        if speed > MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()
        else:
            box2d.revolute_joint_enable_motor(self.front_joint, False)
            box2d.revolute_joint_set_motor_speed(self.back_joint, self.speed)

    def decelerate(self, rate=SPEED_DELTA):
        speed = self.speed - rate
        if speed < -MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()
        else:
            box2d.revolute_joint_set_motor_speed(self.front_joint, self.speed)
            box2d.revolute_joint_enable_motor(self.back_joint, False)

    """
    def accelerate(self, rate=SPEED_DELTA):
        speed = self.speed + rate
        if speed > MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()
        else:
            box2d.revolute_joint_set_motor_speed(
                self.front_joint, self.speed
            )
            box2d.revolute_joint_set_motor_speed(
                self.back_joint, self.speed
            )

    def decelerate(self, rate=SPEED_DELTA):
        speed = self.speed - rate
        if speed < -MAX_SPEED:
            return
        self.speed = speed
        if not self.motors_attached:
            self.attach_motors()
        else:
            box2d.revolute_joint_set_motor_speed(
                self.front_joint, self.speed
            )
            box2d.revolute_joint_set_motor_speed(
                self.back_joint, self.speed
            )
    """

    def coast(self):
        self.detach_motors()
        self.speed = 0

    @debounce(1)
    def ollie(self, impulse=(0, 2.0), point=(0, 0)):
        logger.debug("ollie")
        # Box2D v3's ApplyLinearImpulse takes a *world* point, not a local
        # one, so the local anchor point needs converting first.
        chassis_world_point = box2d.body_get_world_point(  # ASSUMPTION
            self.chassis.body, box2d.Vec2(*point)
        )
        box2d.body_apply_linear_impulse(  # ASSUMPTION
            self.chassis.body, box2d.Vec2(*impulse), chassis_world_point, True
        )

        if self.mountee:
            mountee_world_point = box2d.body_get_world_point(  # ASSUMPTION
                self.mountee.body, box2d.Vec2(*point)
            )
            box2d.body_apply_linear_impulse(  # ASSUMPTION
                self.mountee.body, box2d.Vec2(*impulse), mountee_world_point, True
            )

    def update(self, delta_time=1 / 60):
        super().update(delta_time)
        # No per-frame rate sync needed any more: attach_motors/accelerate/
        # decelerate already push motor_speed to the joints whenever `speed`
        # changes, and Box2D's own step loop reads it from there.
