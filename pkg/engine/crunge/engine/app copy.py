import timeit
import time

from loguru import logger

from crunge import sdl
from crunge import yoga

from .window import Window, DEFAULT_WIDTH, DEFAULT_HEIGHT
from .scheduler import Scheduler
from .service import Service
from .statistics import Statistics

sdl.init(sdl.InitFlags.INIT_VIDEO)


class App(Window):
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        title: str = "Crunge App",
        view=None,
        resizable=False,
    ):
        super().__init__(width, height, title, view=view, resizable=resizable)
        self.running = False
        self.stats = Statistics()
        self.services: list[Service] = []
        self.add_service(Scheduler())

    def add_service(self, service: Service):
        self.services.append(service)

    def remove_service(self, service: Service):
        self.services.remove(service)

    def quit(self):
        self.running = False

    def run(self):
        self.enable()
        self.running = True

        target_dt = 1.0 / 60.0
        last_frame_start = time.perf_counter()

        sdl.start_text_input(self.window)

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
            if sleep_s > 0.0:
                time.sleep(sleep_s)

            frame_end = time.perf_counter()
            frame_s = frame_end - frame_start

            # Legacy fields if needed
            self.frame_time = frame_s
            self.fps = 1.0 / frame_s if frame_s > 0 else 0.0
            self.update_time = update_s
            self.render_time = render_s

            # Stats
            self.stats.timing.push_frame(update_s, render_s, frame_s)
            self.stats.end_frame()

        sdl.stop_text_input(self.window)
        return self

    def apply_layout(self):
        if not self.layout.is_dirty():
            return
        self.layout.calculate_bounds(self.width, self.height, yoga.Direction.LTR)
        # self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        super().apply_layout()

    def update(self, delta_time: float):
        for service in self.services:
            service.update(delta_time)

        self.apply_layout()

        super().update(delta_time)
