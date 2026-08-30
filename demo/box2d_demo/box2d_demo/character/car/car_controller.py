from typing import TYPE_CHECKING

from loguru import logger

from crunge import sdl

from ..character import CharacterController

if TYPE_CHECKING:
    from .car import Car


class CarController(CharacterController):
    def __init__(self, car: "Car"):
        super().__init__(car)
        self.car = car

    def update(self, delta_time: float):
        if self.left_pressed:
            self.car.decelerate()
        elif self.right_pressed:
            self.car.accelerate()
        else:
            self.car.coast()
        super().update(delta_time)

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        match key:
            case sdl.SDLK_w:
                if down and not repeat:
                    self.car.ollie()
            case sdl.SDLK_s:
                if down and not repeat:
                    self.car.dismount()
            case sdl.SDLK_a:
                self.left_pressed = down
            case sdl.SDLK_d:
                self.right_pressed = down
