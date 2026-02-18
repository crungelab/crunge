import pymunk


class CollisionHandler:
    def __init__(
        self, space: pymunk.Space, collision_type_a: int | None = None, collision_type_b: int | None = None
    ):
        space.on_collision(
            collision_type_a,
            collision_type_b,
            begin=self.begin,
            pre_solve=self.pre_solve,
            post_solve=self.post_solve,
            separate=self.separate,
        )

    def begin(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: object):
        return True

    def pre_solve(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: object):
        pass

    def post_solve(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: object):
        pass

    def separate(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: object):
        pass
