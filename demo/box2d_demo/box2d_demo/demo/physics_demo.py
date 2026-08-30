from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import box2d

from crunge.engine.d2.physics import PhysicsWorld2D

from .scrolling_demo import ScrollingDemo
from crunge.engine.d2.physics.world_debug_overlay import WorldDebugOverlay


class PhysicsDemo(ScrollingDemo):
    def create_display(self):
        super().create_display()
        self.debug_overlay = WorldDebugOverlay()
        #self.display.add_overlay(self.debug_overlay)
        self.display.primary_view.add_overlay(self.debug_overlay)

    def create_world(self):
        self.world = PhysicsWorld2D()
        self.world.make_current()

    def reset(self):
        super().reset()

        self.debug_draw_enabled = False

        self.create_world()

        # Mouse drag state — kinematic body follows mouse position
        body_def = box2d.BodyDef(type=box2d.BodyType.KINEMATIC_BODY)
        self._mouse_body = self.world.create_body(body_def)
        self._mouse_joint = None
        self._dragged_body = None

    def update(self, delta_time: float):
        self.world.update(1 / 60)
        super().update(delta_time)

    # ------------------------------------------------------------------
    # Drag helpers
    # ------------------------------------------------------------------

    def _screen_to_world(self, x: float, y: float):
        return self.camera.unproject(glm.vec2(x, y))

    def _box2d_pos(self, world):
        return box2d.Vec2(world.x, world.y)

    def _begin_drag(self, x: float, y: float):
        if self._mouse_joint is not None:
            return False

        world = self._screen_to_world(x, y)
        target = self._box2d_pos(world)

        hit = None

        def overlap_callback(shape):
            nonlocal hit
            body = shape.body
            if body.get_type() != box2d.BodyType.DYNAMIC_BODY:
                return True  # keep searching
            if not shape.test_point(target):  # ASSUMPTION: b2Shape_TestPoint binding
                return True
            hit = shape
            return False  # first exact hit wins — stop the query

        # Point proxy: no halo. Exact containment only.
        proxy = box2d.make_proxy(target, 1, 0.0)

        origin = box2d.Vec2(0, 0)
        self.world.overlap_shape(origin, proxy, box2d.default_query_filter(), overlap_callback)

        if hit is None:
            return False

        body = hit.body
        self._dragged_body = body
        body.set_awake(True)

        self._mouse_body.set_transform(target, box2d.make_rot(0.0))

        joint_def = box2d.DistanceJointDef(
            body_id_a=self._mouse_body,
            body_id_b=body,
            local_frame_a=box2d.Transform(p=self._mouse_body.get_local_point(target)),
            local_frame_b=box2d.Transform(p=body.get_local_point(target)),
            length=0.25,
            enable_spring=True,
            hertz=2.5,
            damping_ratio=0.5,
        )
        self._mouse_joint = self.world.create_distance_joint(joint_def)
        logger.debug(f"Drag started on {hit} at {target}")
        return True

    def _end_drag(self):
        if self._mouse_joint is not None:
            box2d.destroy_joint(self._mouse_joint)
            self._mouse_joint = None
        self._dragged_body = None

    def _update_drag(self, x: float, y: float):
        if self._mouse_joint is not None:
            world = self._screen_to_world(x, y)
            # Move the kinematic mouse body; the joint pulls the dynamic body along
            self._mouse_body.set_transform(self._box2d_pos(world), box2d.make_rot(0.0))

    @property
    def is_dragging(self):
        return self._mouse_joint is not None

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        self._update_drag(event.x, event.y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button == 3:  # ← right mouse button
            if event.down:
                self._begin_drag(event.x, event.y)
            else:
                self._end_drag()

    # ------------------------------------------------------------------
    # Draw & UI
    # ------------------------------------------------------------------

    def draw_physics_options(self):
        _, self.debug_draw_enabled = imgui.checkbox(
            "Debug Draw", self.debug_draw_enabled
        )
        self.debug_overlay.visible = self.debug_draw_enabled
