from .sprite import Sprite


DEFAULT_DURATION = 1/12


class SpriteAnimationFrame:
    def __init__(self, sprite: Sprite, duration: float = DEFAULT_DURATION):
        self.sprite = sprite
        self.duration = duration


class SpriteAnimation:
    def __init__(self, name: str):
        self.name = name
        self.frames: list[SpriteAnimationFrame] = []
        self.current_frame = 0
        self.time = 0
        self.speed = 1
        self.loop = True
        self.playing = False

    def mirror(self, name: str, horizontal: bool = False, vertical: bool = False):
        other = SpriteAnimation(name)
        for frame in self.frames:
            other.add_frame(SpriteAnimationFrame(frame.sprite.mirror(horizontal, vertical), frame.duration))
        return other

    def add_frame(self, frame):
        self.frames.append(frame)

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def update(self, dt):
        if self.playing:
            self.time += dt * self.speed
            if self.time >= self.frames[self.current_frame].duration:
                self.time = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    if self.loop:
                        self.current_frame = 0
                    else:
                        self.playing = False
