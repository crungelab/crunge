I decided to pass the renderer to each draw call because
A.  Dependency injection was too painful
B.  Globals are problematic also

With this design we can either render to the swapchain texture or an offscreen texture.