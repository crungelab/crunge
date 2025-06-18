from crunge import wgpu


class Binding:
    def __init__(self, binding: int):
        if not isinstance(binding, int) or binding < 0:
            raise ValueError("Binding must be a non-negative integer.")
        self.binding = binding

    def to_bind_group_entry(self) -> wgpu.BindGroupEntry:
        """Converts the Binding object to a wgpu.BindGroupEntry dictionary."""
        raise NotImplementedError("Subclasses must implement to_bind_group_entry.")


class UniformBinding(Binding):
    def __init__(
        self, binding: int, buffer: wgpu.GPUBuffer, offset: int = 0, size: int = None
    ):
        super().__init__(binding)
        if not isinstance(buffer, wgpu.GPUBuffer):
            raise TypeError("buffer must be a wgpu.GPUBuffer.")
        self.buffer = buffer
        self.offset = offset
        self.size = size if size is not None else buffer.size

    def to_bind_group_entry(self) -> wgpu.BindGroupEntry:
        return wgpu.BindGroupEntry(
            binding=self.binding,
            buffer=self.buffer,
            size=self.size,
        )


class TextureBinding(Binding):
    def __init__(self, binding: int, texture_view: wgpu.TextureView):
        super().__init__(binding)
        if not isinstance(texture_view, wgpu.TextureView):
            raise TypeError("texture_view must be a wgpu.GPUTextureView.")
        self.texture_view = texture_view

    def to_bind_group_entry(self) -> wgpu.BindGroupEntry:
        return wgpu.BindGroupEntry(binding=self.binding, texture_view=self.texture_view)


class SamplerBinding(Binding):
    def __init__(self, binding: int, sampler: wgpu.Sampler):
        super().__init__(binding)
        if not isinstance(sampler, wgpu.Sampler):
            raise TypeError("sampler must be a wgpu.GPUSampler.")
        self.sampler = sampler

    def to_bind_group_entry(self) -> wgpu.BindGroupEntry:
        return wgpu.BindGroupEntry(binding=self.binding, sampler=self.sampler)
