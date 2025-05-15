from crunge import wgpu


def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device
    print(device)

if __name__ == "__main__":
    main()