from typing import List, Dict
import timeit
import sys, time
import math

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from .window import Window, DEFAULT_WIDTH, DEFAULT_HEIGHT
from .scheduler import Scheduler
from .service import Service


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
        self.services: List[Service] = []
        self.add_service(Scheduler())

    def add_service(self, service: Service):
        self.services.append(service)

    def remove_service(self, service: Service):
        self.services.remove(service)

    def create_window(self):
        # success = sdl.init(sdl.InitFlags.INIT_VIDEO)
        # logger.debug(f"SDL_Init: {success}")
        super().create_window()

    def quit(self):
        self.running = False

    def run(self):
        self.enable()
        self.running = True

        target_frame_time = 1 / 60  # 60 FPS
        last_time = time.perf_counter()

        sdl.start_text_input(self.window)

        while self.running:
            # --- Mark the start of the frame
            frame_start = time.perf_counter()

            self.instance.process_events()

            while event := sdl.poll_event():
                self.dispatch(event)
                if event.type == sdl.EventType.QUIT:
                    self.running = False

            # Compute frame delta
            now = time.perf_counter()
            frame_time = now - last_time

            # Game update & render
            update_start_time = timeit.default_timer()
            self.update(frame_time)
            self.update_time = timeit.default_timer() - update_start_time

            frame_start_time = timeit.default_timer()
            self.frame()
            self.frame_time = timeit.default_timer() - frame_start_time

            # Calculate how much time is left to maintain 60 FPS
            elapsed = time.perf_counter() - frame_start
            time_left = target_frame_time - elapsed
            if time_left > 0:
                time.sleep(time_left)

            # Set up for next frame
            last_time = frame_start

        sdl.stop_text_input(self.window)
        return self

    def apply_layout(self):
        if not self.layout.is_dirty():
            return
        self.layout.calculate_bounds(self.width, self.height, yoga.Direction.LTR)
        #self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        super().apply_layout()
    
    def update(self, delta_time: float):
        for service in self.services:
            service.update(delta_time)

        self.apply_layout()

        super().update(delta_time)
