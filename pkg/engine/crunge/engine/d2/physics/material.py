from crunge import box2d


class PhysicsMaterial:
    """Surface properties plus a stable id for contact identification."""

    _next_id = 1
    _by_id: dict[int, "PhysicsMaterial"] = {}

    def __init__(
        self,
        name: str,
        friction: float = 0.6,
        restitution: float = 0.0,
        rolling_resistance: float = 0.0,
        tangent_speed: float = 0.0,
        custom_color: int = 0,
    ) -> None:
        self.name = name
        self.friction = friction
        self.restitution = restitution
        self.rolling_resistance = rolling_resistance
        self.tangent_speed = tangent_speed
        self.custom_color = custom_color

        self.id = PhysicsMaterial._next_id
        PhysicsMaterial._next_id += 1
        PhysicsMaterial._by_id[self.id] = self

    @classmethod
    def get(cls, material_id: int) -> "PhysicsMaterial | None":
        return cls._by_id.get(material_id)

    def apply(self, shape_def) -> None:
        m = shape_def.material
        m.friction = self.friction
        m.restitution = self.restitution
        m.rolling_resistance = self.rolling_resistance
        m.tangent_speed = self.tangent_speed
        m.custom_color = self.custom_color
        m.user_material_id = self.id

        # print(f"PhysicsMaterial.apply: {self.name} -> {shape_def}")

    def apply_chain(self, chain_def) -> None:
        chain_def.materials = box2d.SurfaceMaterial(
            friction=self.friction,
            restitution=self.restitution,
            rolling_resistance=self.rolling_resistance,
            tangent_speed=self.tangent_speed,
            user_material_id=self.id,
            custom_color=self.custom_color,
        )

    """
    def apply_chain(self, chain_def) -> None:
        material = box2d.SurfaceMaterial(
            friction=self.friction,
            restitution=self.restitution,
            rolling_resistance=self.rolling_resistance,
            tangent_speed=self.tangent_speed,
            user_material_id=self.id,
            custom_color=self.custom_color,
        )
        chain_def.materials = [material]  # ASSUMPTION: wrapper takes a list
        chain_def.material_count = 1
    """

    def __repr__(self) -> str:
        return f"<PhysicsMaterial {self.name} id={self.id}>"


DEFAULT_MATERIAL = PhysicsMaterial("default")
