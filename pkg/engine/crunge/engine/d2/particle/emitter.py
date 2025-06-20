class Emitter:
    def __init__(self, system, spawner, rate=0, burst_count=0):
        self.system = system
        self.spawner = spawner
        self.rate = rate  # particles per second
        self.burst_count = burst_count
        self.accumulator = 0.0
        self.burst_done = False

    def update(self, dt):
        if self.burst_count > 0 and not self.burst_done:
            self.emit_burst(self.burst_count)
            self.burst_done = True
        elif self.rate > 0:
            self.accumulator += dt * self.rate
            while self.accumulator >= 1.0:
                self.emit(1)
                self.accumulator -= 1.0

    def emit(self, count):
        for _ in range(count):
            index = self.system.acquire_particle_index()
            if index is not None:
                self.spawner(self.system.particles[index])

    def emit_burst(self, count):
        self.emit(count)
