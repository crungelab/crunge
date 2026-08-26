import gc
import timeit
import time

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from .window import Window, DEFAULT_WIDTH, DEFAULT_HEIGHT
from .scheduler import Scheduler
from .service import Service
from .statistics import Statistics

sdl.init(sdl.InitFlags.INIT_VIDEO)

# Minimum idle slack (seconds) required before we'll spend time on a
# manual gen-0 collection. Tune against measured gc.collect(0) cost.
GC_MIN_SLACK_S = 0.001

# How many frames to wait between manual gen-0 collections when there's
# slack available. Keeps collection cheap and infrequent rather than
# scanning every frame.
GC_INTERVAL_FRAMES = 30


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
        self.add_service(Scheduler())

        # Disable the automatic cyclic GC. We'll trigger gen-0 collections
        # ourselves during frames that have spare time, instead of letting
        # the collector fire at unpredictable (and possibly expensive)
        # moments mid-frame.
        gc.disable()
        self._gc_frame_counter = 0

    def add_service(self, service: Service):
        self.services.append(service)

    def remove_service(self, service: Service):
        self.services.remove(service)

    def quit(self):
        self.running = False

    def run(self):
        self.make_current() # TODO: This should be in _enable() or similar, not run()
        self.enable()
        self.running = True

        target_dt = 1.0 / 60.0
        last_frame_start = time.perf_counter()

        sdl.start_text_input(self.window)

        # Let init-time allocations (services, resource manager, scene
        # scaffolding, etc.) settle, then freeze them out of future
        # collections so the collector only ever scans per-frame churn.
        gc.collect()
        gc.freeze()

        while self.running:
            frame_start = time.perf_counter()
            dt = frame_start - last_frame_start
            if dt <= 0.0:
                dt = 1e-12
            last_frame_start = frame_start

            self.stats.begin_frame()

            # Events
            self.instance.process_events()
            while event := sdl.poll_event():
                self.dispatch(event)
                if event.type == sdl.EventType.QUIT:
                    self.running = False

            # Update
            t0 = time.perf_counter()
            self.update(dt)
            update_s = time.perf_counter() - t0

            # Render
            t0 = time.perf_counter()
            self.frame()
            render_s = time.perf_counter() - t0

            # Frame cap
            work_end = time.perf_counter()
            work_s = work_end - frame_start
            sleep_s = target_dt - work_s

            # Spend a slice of any spare time on a manual gen-0 GC pass
            # instead of sleeping through all of it. Only bother when
            # there's comfortably enough slack, and don't do it every
            # frame -- gen-0 collection is cheap but not free.
            gc_s = 0.0
            self._gc_frame_counter += 1
            if sleep_s > GC_MIN_SLACK_S and self._gc_frame_counter >= GC_INTERVAL_FRAMES:
                self._gc_frame_counter = 0
                t0 = time.perf_counter()
                gc.collect(generation=0)
                gc_s = time.perf_counter() - t0
                sleep_s -= gc_s

            if sleep_s > 0.0:
                time.sleep(sleep_s)

            frame_end = time.perf_counter()
            frame_s = frame_end - frame_start

            # Legacy fields if needed
            self.frame_time = frame_s
            self.fps = 1.0 / frame_s if frame_s > 0 else 0.0
            self.update_time = update_s
            self.render_time = render_s
            self.gc_time = gc_s

            # Stats
            self.stats.timing.push_frame(update_s, render_s, frame_s)
            self.stats.end_frame()

        sdl.stop_text_input(self.window)
        return self

    """
    def apply_layout(self):
        size = self.size
        if not self.layout.is_dirty() and self._layout_size == size:
            return
        self._layout_size = glm.ivec2(size)
        self.layout.calculate_bounds(size.x, size.y, yoga.Direction.LTR)
        logger.debug(f"apply_layout: size={size} layout_size={self._layout_size} dirty={self.layout.is_dirty()}")

        super().apply_layout()

        new_size = self.size
        logger.debug(f"Window size: {new_size}")
        logger.debug(f"Framebuffer size: {self.easel.size}")
    """

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