class RenderOptions:
    def __init__(
        self,
        use_depth_stencil: bool = False,
        use_msaa: bool = False,
        use_snapshot: bool = False,
    ):
        self.use_depth_stencil = use_depth_stencil
        self.use_msaa = use_msaa
        self.sample_count = 4 if use_msaa else 1
        self.use_snapshot = use_snapshot
