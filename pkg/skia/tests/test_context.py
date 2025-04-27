from crunge import wgpu
from crunge import skia

def main():
    # Create a WGPU context
    wgpu_context = wgpu.Context()
    assert wgpu_context is not None, "Failed to create WGPU context"

    # Create a Skia context
    skia_context = skia.create_context(wgpu_context.instance, wgpu_context.device)
    assert skia_context is not None, "Failed to create Skia context"

    # Clean up contexts
    #wgpu_context.destroy()
    #skia_context.destroy()

if __name__ == "__main__":
    main()