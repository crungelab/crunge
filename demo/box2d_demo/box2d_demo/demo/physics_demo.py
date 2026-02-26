from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import box2d

#from box2d_demo.physics.draw_options import DrawOptions
from box2d_demo.physics import DynamicPhysicsEngine

from .scrolling_demo import ScrollingDemo


class PhysicsDemo(ScrollingDemo):
    """
    def __init__(self):
        super().__init__()
        self.create_physics_engine()
    """

    def create_physics_engine(self):
        self.world = DynamicPhysicsEngine()
        self.world.make_current()

    def reset(self):
        super().reset()

        self.debug_draw_enabled = False
        #self.draw_options = DrawOptions(self.view.scratch)

        self.create_physics_engine()

        # Mouse drag state
        #self._mouse_body = box2d.Body(body_type=box2d.BodyType.KINEMATIC_BODY)
        body_def = box2d.BodyDef(type=box2d.BodyType.KINEMATIC_BODY)
        self._mouse_body = self.world.create_body(body_def)
        #self.physics_engine.world.add(self._mouse_body)
        self._mouse_joint = None
        self._dragged_shape = None

    """
    def run(self):
        with self.world.use():
            super().run()
    """

    # ------------------------------------------------------------------
    # Drag helpers
    # ------------------------------------------------------------------

    def _screen_to_world(self, x: float, y: float):
        return self.camera.unproject(glm.vec2(x, y))

    def _box2d_pos(self, world):
        return (world.x, world.y)

    def _begin_drag(self, x: float, y: float):
        world = self._screen_to_world(x, y)
        pm_pos = self._box2d_pos(world)

        hit = self.world.world.point_query_nearest(
            pm_pos, max_distance=5, shape_filter=box2d.ShapeFilter()
        )
        if hit is None or hit.shape is None:
            return False

        body = hit.shape.body
        if body.body_type != box2d.BodyType.DYNAMIC_BODY:
            return False

        self._dragged_shape = hit.shape
        self._mouse_body.position = pm_pos

        self._mouse_joint = box2d.PivotJoint(self._mouse_body, body, pm_pos)
        self._mouse_joint.max_force = 50_000
        self._mouse_joint.error_bias = pow(1.0 - 0.15, 60)
        self.world.world.add(self._mouse_joint)

        logger.debug(f"Drag started on {hit.shape} at {pm_pos}")
        return True

    def _update_drag(self, x: float, y: float):
        if self._mouse_joint is not None:
            world = self._screen_to_world(x, y)
            self._mouse_body.position = self._box2d_pos(world)

    def _end_drag(self):
        if self._mouse_joint is not None:
            self.world.world.remove(self._mouse_joint)
            self._mouse_joint = None
            self._dragged_shape = None
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

    def _draw(self):
        if self.debug_draw_enabled:
            self.world.debug_draw(self.draw_options)
        super()._draw()

    def draw_physics_options(self):
        _, self.debug_draw_enabled = imgui.checkbox(
            "Debug Draw", self.debug_draw_enabled
        )
