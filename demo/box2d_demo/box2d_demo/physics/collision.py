from crunge import box2d


class CollisionHandler:
    def __init__(
        self, space: box2d.World, collision_type_a: int | None = None, collision_type_b: int | None = None
    ):
        space.on_collision(
            collision_type_a,
            collision_type_b,
            begin=self.begin,
            pre_solve=self.pre_solve,
            post_solve=self.post_solve,
            separate=self.separate,
        )

    def begin(self, arbiter: box2d.Arbiter, space: box2d.World, data: object):
        return True

    def pre_solve(self, arbiter: box2d.Arbiter, space: box2d.World, data: object):
        pass

    def post_solve(self, arbiter: box2d.Arbiter, space: box2d.World, data: object):
        pass

    def separate(self, arbiter: box2d.Arbiter, space: box2d.World, data: object):
        pass
