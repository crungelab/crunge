import time

from loguru import logger

from crunge import sdl
from crunge import yoga

from .window import Window, DEFAULT_WIDTH, DEFAULT_HEIGHT
from .updater import Updater
from .scheduler import Scheduler
from .service import Service
from .statistics import Statistics

sdl.init(sdl.InitFlags.INIT_VIDEO)

# Upper bound on the delta_time handed to update(). A frame that runs long
# -- a lazy pipeline compile, a texture upload, the window being dragged --
# would otherwise integrate as one enormous step: the camera lurches, physics
# tunnels, lerps snap straight to target. Clamping trades a moment of slow
# motion for continuity, which is the better artifact.
MAX_FRAME_TIME = 0.25


class App(Window):
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        title: str = "Crunge App",
        display=None,
        resizable=False,
    ):
        super().__init__(width, height, title, display=display, resizable=resizable)
        self.running = False
        self.stats = Statistics()
        self.services: list[Service] = []

        self.add_service(Updater())
        self.add_service(Scheduler())

        # Seeded so anything reading these during the first frame -- a stats
        # overlay drawn from inside frame() -- sees zeros rather than raising.
        self.frame_time = 0.0
        self.update_time = 0.0
        self.render_time = 0.0
        self.fps = 0.0

    def add_service(self, service: Service):
        self.services.append(service)

    def remove_service(self, service: Service):
        self.services.remove(service)

    def quit(self):
        self.running = False

    def run(self):
        self.make_current()  # TODO: This should be in _enable() or similar, not run()
        self.enable()
        self.reset()

        self.running = True
        last_frame_start = time.perf_counter()

        sdl.start_text_input(self.sdl_window)
        try:
            while self.running:
                frame_start = time.perf_counter()
                delta_time = frame_start - last_frame_start
                last_frame_start = frame_start
                delta_time = min(max(delta_time, 1e-12), MAX_FRAME_TIME)

                self.stats.begin_frame()

                # Events
                self.instance.process_events()
                while event := sdl.poll_event():
                    self.dispatch(event)
                    if event.type == sdl.EventType.QUIT:
                        self.running = False

                # Update
                t0 = time.perf_counter()
                self.update(delta_time)
                update_s = time.perf_counter() - t0

                # Render
                t0 = time.perf_counter()
                self.frame()
                render_s = time.perf_counter() - t0

                # No sleep-based frame cap: the surface presents with Fifo, so
                # frame() already blocks until the vblank. A second limiter on
                # top of vsync only pushes work up against the interval
                # boundary, where it randomly makes it or misses.
                frame_s = time.perf_counter() - frame_start

                self.frame_time = frame_s
                self.update_time = update_s
                self.render_time = render_s
                self.fps = 1.0 / frame_s if frame_s > 0.0 else 0.0

                # Stats
                self.stats.timing.push_frame(update_s, render_s, frame_s)
                self.stats.end_frame()
        finally:
            sdl.stop_text_input(self.sdl_window)

        return self

    def apply_layout(self):
        if not self.layout.is_dirty():
            return
        self.layout.calculate_bounds(self.width, self.height, yoga.Direction.LTR)
        super().apply_layout()

    def update(self, delta_time: float):
        for service in self.services:
            service.update(delta_time)

        self.apply_layout()

        super().update(delta_time)