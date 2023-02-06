from crunge import wgpu

def main():
    usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.COPY_SRC
    print(int(usage))

if __name__ == "__main__":
    main()
