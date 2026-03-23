from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import box2d

from box2d_demo.physics.debug_draw import DebugDraw
from box2d_demo.physics import DynamicPhysicsEngine

from .scrolling_demo import ScrollingDemo
from ..physics.world_debug_overlay import WorldDebugOverlay


class PhysicsDemo(ScrollingDemo):
    def create_view(self):
        super().create_view()
        self.debug_overlay = WorldDebugOverlay()
        self.view.add_overlay(self.debug_overlay)

    def create_physics_engine(self):
        self.world = DynamicPhysicsEngine()
        self.world.make_current()

    def reset(self):
        super().reset()

        self.debug_draw_enabled = False
        self.debug_draw = DebugDraw()

        self.create_physics_engine()

        # Mouse drag state — kinematic body follows mouse position
        body_def = box2d.BodyDef(type=box2d.BodyType.KINEMATIC_BODY)
        self._mouse_body = self.world.create_body(body_def)
        self._mouse_joint = None
        self._dragged_body = None

    # ------------------------------------------------------------------
    # Drag helpers
    # ------------------------------------------------------------------

    def _screen_to_world(self, x: float, y: float):
        return self.camera.unproject(glm.vec2(x, y))

    def _box2d_pos(self, world):
        return box2d.Vec2(world.x, world.y)

    def _begin_drag(self, x: float, y: float):
        world = self._screen_to_world(x, y)
        target = self._box2d_pos(world)

        """
        b2Circle circle = {b2Vec2_zero, 0.2f};
        b2ShapeProxy proxy = b2MakeProxy(&circle.center, 1, circle.radius);
        b2World_OverlapShape(myWorldId, &proxy, grenadeFilter, MyOverlapCallback, &myGame);
        """
        hit = None
        def overlap_callback(shape):
            logger.debug(f"Overlap callback: {shape}")
            nonlocal hit
            hit = shape
            return True

        circle = box2d.Circle(center=target, radius=0.2)
        proxy = box2d.make_proxy(circle.center, 1, circle.radius)
        self.world.overlap_shape(proxy, box2d.default_query_filter(), overlap_callback)
        '''
        hit = self.world.point_query_nearest(
            target, max_distance=0.001, shape_filter=box2d.ShapeFilter()
        )
        '''
        if hit is None:
            return False

        body = hit.body
        logger.debug(f"Hit body: {body}, index: {body.index1}")
        if body.get_type() != box2d.BodyType.DYNAMIC_BODY:
            return False

        self._dragged_body = body
        body.set_awake(True)

        # Place the mouse body exactly at the click point
        self._mouse_body.set_transform(target, box2d.make_rot(0.0))
        logger.debug(f"Mouse body: {self._mouse_body}, index: {self._mouse_body.index1}")

        joint_def = box2d.DistanceJointDef(
            #body_a=self._mouse_body,
            #body_b=body,
            #local_anchor_a=(0.0, 0.0),
            #local_anchor_b=body.get_local_point(target),
            length=0.1,
            min_length=0.1,
            max_length=0.2,
            frequency_hz=5.0,
            damping_ratio=0.7,
        )
        joint_def.base.body_id_a = self._mouse_body
        joint_def.base.body_id_b = body
        joint_def.base.local_frame_a = box2d.Transform(box2d.Vec2(0.0, 0.0), box2d.make_rot(0.0))
        joint_def.base.local_frame_b.p = body.get_local_point(target)

        self._mouse_joint = self.world.create_distance_joint(joint_def)

        logger.debug(f"Drag started on {hit} at {target}")
        return True

    def _update_drag(self, x: float, y: float):
        if self._mouse_joint is not None:
            world = self._screen_to_world(x, y)
            # Move the kinematic mouse body; the joint pulls the dynamic body along
            self._mouse_body.set_transform(self._box2d_pos(world), box2d.make_rot(0.0))

    def _end_drag(self):
        if self._mouse_joint is not None:
            box2d.destroy_joint(self._mouse_joint, False)
            self._mouse_joint = None
            self._dragged_body = None
            logger.debug("Drag ended")

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
