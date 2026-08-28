import math
import random

from loguru import logger
import cairo

from crunge.engine.d2.sprite import Sprite
from crunge.engine.resource.resource_manager import ResourceManager

from . import engine

from .beacon import Beacon

from wyggles import Dna
from wyggles import SpriteNode, SpriteFactory

PI = math.pi
RADIUS = 32
WIDTH = RADIUS
HEIGHT = RADIUS

class FruitDna(Dna):
    def __init__(self, klass):
        super().__init__(klass)
        self.sprites = []
        self.create_sprites()

    def create_sprites(self):
        #surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        path = f"${{images}}/{self.kind}.png"
        resolved_path = ResourceManager().resolve_path(path)
        surface = cairo.ImageSurface.create_from_png(resolved_path)

        ctx = cairo.Context(surface)
        ctx.scale(1, 1)  # Normalizing the canvas

        imgsize = (WIDTH, HEIGHT) #The size of the image

        texture = self.create_texture(surface, f"{self.kind}_0", imgsize)
        logger.debug(f"Texture created for {self.kind}: {texture}")
        self.sprites.append(Sprite(texture))

        for y in range(2):
            for x in range(2):
                self.draw_bite(ctx, x * 32, y * 32)
                texture = self.create_texture(surface, f"{self.kind}_{x+y}", imgsize)
                self.sprites.append(Sprite(texture))

    def draw_bite(self, ctx, x, y):
        ctx.arc(x, y, 16, 0, PI * 2)
        ctx.close_path()
        #pat = cairo.SolidPattern(0, 0, 0, alpha=0)
        #ctx.set_source(pat)
        ctx.set_operator(cairo.Operator.CLEAR)
        ctx.fill()


#
class Fruit(SpriteNode):
    def __init__(self, dna):
        super().__init__(dna)
        self.type = dna.kind
        self.energy = 5
        self.beacon = Beacon(self, self.type)
        engine.sprite_engine.add_beacon(self.beacon)
        self.model = dna.sprites[0]

    def receive_munch(self):
        self.energy -= 1
        if(self.energy <= 0):
            engine.sprite_engine.remove_beacon(self.beacon)
            #self.layer.detach(self)
            self.destroy()
            return 0.01
        #else
        self.model = self.dna.sprites[5 - self.energy]
        return 0.01

    def is_munched(self):
        return self.energy <= 0


class Apple(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))


class Banana(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))


class Grape(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))


class Orange(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))


class Pineapple(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))


class Strawberry(Fruit):
    def __init__(self):
        super().__init__(FruitDna(self.__class__))



class FruitFactory(SpriteFactory):
    def __init__(self, layer):
        super().__init__(layer)

    def create_random(self):
        return list(kinds.values())[random.randint(0, 5)]()

kinds = {
    'apple': Apple,
    'banana': Banana,
    'grape': Grape,
    'orange': Orange,
    'pineapple': Pineapple,
    'strawberry': Strawberry
}