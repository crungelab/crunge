from crunge import wgpu

def main():
    usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.COPY_SRC
    print(int(usage))

    visibility = wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT
    print(int(visibility))

if __name__ == "__main__":
    main()
