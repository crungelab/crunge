from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    #usage = wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC
    #usage = wgpu.TextureUsage.RENDER_ATTACHMENT
    usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.COPY_SRC
    print(int(usage))

if __name__ == "__main__":
    main()
