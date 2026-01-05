from crunge import wgpu

def main():
    extent = wgpu.Extent3D(width=1, height=1, depth_or_array_layers=1)
    print(extent.width)
    print(extent.height)
    print(extent.depth_or_array_layers)

if __name__ == "__main__":
    main()
