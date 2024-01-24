import sys, time

from loguru import logger

from crunge import sdl

from .window import Window
from .view import View

class App(Window):
    def __init__(self, width, height, title="", resizable=False):
        super().__init__(width, height, title, resizable)
        self.view = None
        self.callbacks = []

    def create_window(self):
        success = sdl.init(sdl.InitFlags.INIT_VIDEO)
        logger.info(f"SDL_Init: {success}")
        super().create_window()
    
    def schedule_once(self, callback, delay):
        #self.callbacks.append((callback, delay))
        self.callbacks.append(callback)

    def run(self):
        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        running = True
        while running:
            #TODO: !wasAlreadyWaited
            #self.instance.process_events()

            while event := sdl.poll_event():
                if not self.dispatch(event):
                    running = False

            now = time.perf_counter()
            frame_time = now - last_time

            # Calculate how much time is left to delay to maintain 60 FPS
            time_left = target_frame_time - frame_time

            # If there's time left in this frame, delay the next frame
            if time_left > 0:
                time.sleep(time_left)

            # Update last_time for the next frame, considering the sleep
            last_time = time.perf_counter()

            self.frame()

            for callback in self.callbacks:
                callback(frame_time)
            self.callbacks.clear()
