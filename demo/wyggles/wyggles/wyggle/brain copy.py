import math
import random

from loguru import logger
import glm

from wyggles.sprite_node import SpriteNode

from .. import engine
from wyggles.brain import Brain


class WyggleBrain(Brain):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.focus: SpriteNode = None
        self.state: str = "wanderer"
        self.consider_max = 10
        self.consider_timer = self.consider_max
        #
        self.wiggle_phase = 0.0
        self.munch_timer = 10

    def reset(self):
        self.state = ""
        self.focus = None

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)

    def move(self):
        #max_speed = 2.0
        max_speed = 1.0
        avoidance_force = 4.0
        avoidance_distance = 48
        agent_radius = 16
        wiggle_strength = 0.6    # Try 0.2 .. 1.2 for subtle to wild wiggle
        wiggle_speed = 0.25      # Higher = faster wiggle

        # --- Step 1: Seek target ---
        to_target = self.target_position - self.node.position
        if glm.length(to_target) > 1e-3:
            seek_velocity = glm.normalize(to_target) * max_speed
        else:
            seek_velocity = glm.vec2(0, 0)

        # --- Step 2: Obstacle avoidance (look ahead) ---
        current_position = pymunk.Vec2d(self.node.position.x, self.node.position.y)
        if glm.length(to_target) > 1e-3:
            look_ahead = glm.normalize(to_target) * avoidance_distance
        else:
            look_ahead = glm.vec2(0, 0)
        ahead_position = self.node.position + look_ahead
        end_position = pymunk.Vec2d(ahead_position.x, ahead_position.y)
        space = engine.sprite_engine.space

        avoidance = glm.vec2(0, 0)
        results = space.segment_query(current_position, end_position, agent_radius, pymunk.ShapeFilter())
        for result in results:
            node = result.shape.body.node
            if node == self.node or node == self.focus:
                continue
            normal = result.normal
            avoidance += glm.normalize(glm.vec2(normal.x, normal.y)) * avoidance_force
            #break  # Only avoid first obstacle

        # --- Step 3: Combine steering ---
        steering_vec = seek_velocity + avoidance
        if glm.length(steering_vec) > 1e-3:
            steering_dir = glm.normalize(steering_vec)
        else:
            steering_dir = glm.vec2(1, 0)  # Arbitrary default

        # --- Step 4: Add wormy wiggle ---
        # Maintain a wiggle phase per worm
        self.wiggle_phase += wiggle_speed

        # Get perpendicular to current steering
        perp = glm.vec2(-steering_dir.y, steering_dir.x)
        # Sinusoidal "wiggle" in the perpendicular direction
        steering_dir += perp * math.sin(self.wiggle_phase) * wiggle_strength

        # Clamp to max speed
        final_velocity = glm.normalize(steering_dir) * max_speed
        self.velocity = final_velocity

        # --- Step 5: Move the agent ---
        next_position = self.node.position + final_velocity
        self.node.move(next_position)

    '''
    def left(self, angle):
        heading = self.heading - angle
        self.heading = heading if heading > 0 else 360 + heading

    def right(self, angle):
        heading = self.heading + angle
        self.heading = heading if heading < 359 else heading - 360

    def forward(self, distance):
        x, y = self.position
        px = x + (distance * (math.cos(glm.radians(self.heading))))
        py = y + (distance * (math.sin(glm.radians(self.heading))))
        self.move_to(glm.vec2(px, py))

    def randforward(self):
        self.forward(random.randint(0, self.sensor_range))
    '''

    def get_clear_wander_direction(self):
        max_angle_offset = 90  # degrees
        n_samples = 6
        stride = self.sensor_range

        current_heading = self.heading  # or derive from velocity or steering direction
        logger.debug(f"Current heading: {current_heading}")

        # Gather candidate angles
        candidate_angles = [
            current_heading + random.uniform(-max_angle_offset, max_angle_offset)
            for _ in range(n_samples)
        ]

        clear_candidates = []

        for angle in candidate_angles:
            # Convert to direction vector
            radians = glm.radians(angle)
            direction = glm.vec2(math.cos(radians), math.sin(radians))
            start = pymunk.Vec2d(self.node.position.x, self.node.position.y)
            end_pos = self.node.position + direction * stride
            end = pymunk.Vec2d(end_pos.x, end_pos.y)

            results = engine.sprite_engine.space.segment_query(
                start, end, self.node.radius, pymunk.ShapeFilter()
            )
            '''
            if not any(result.shape.body.node != self.node for result in results):
                clear_candidates.append(angle)
            '''
            if not results:
                clear_candidates.append(angle)

        if clear_candidates:
            return random.choice(clear_candidates)
        else:
            # All directions blocked; fallback to current heading or slow down
            return current_heading
