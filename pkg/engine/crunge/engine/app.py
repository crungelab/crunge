from typing import List, Dict
import sys, time

from loguru import logger
import glm

from crunge import sdl

from .window import Window
from .scheduler import Scheduler
from .service import Service
#from .channel import Channel


class App(Window):
    def __init__(self, size=glm.ivec2(), title="", view=None, resizable=False):
        super().__init__(size, title, view=view, resizable=resizable)
        self.running = False
        self.services: List[Service] = []
        self.add_service(Scheduler())

    def add_service(self, service: Service):
        self.services.append(service)

    def remove_service(self, service: Service):
        self.services.remove(service)
    
    def create_window(self):
        success = sdl.init(sdl.InitFlags.INIT_VIDEO)
        logger.debug(f"SDL_Init: {success}")
        super().create_window()

    def quit(self):
        self.running = False

    def run(self):
        self.running = True

        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        sdl.start_text_input(self.window)

        while self.running:
            self.instance.process_events()

            while event := sdl.poll_event():
                self.dispatch(event)
                if event.type == sdl.EventType.QUIT:
                    self.running = False

            now = time.perf_counter()
            frame_time = now - last_time

            # Calculate how much time is left to delay to maintain 60 FPS
            time_left = target_frame_time - frame_time

            # If there's time left in this frame, delay the next frame
            if time_left > 0:
                time.sleep(time_left)

            # Update last_time for the next frame, considering the sleep
            last_time = time.perf_counter()

            self.update(frame_time)

            self.frame()

        sdl.stop_text_input(self.window)
        # self.device.destroy()
        return self

    def update(self, delta_time: float):
        #Scheduler().update(delta_time)
        for service in self.services:
            service.update(delta_time)
        super().update(delta_time)
