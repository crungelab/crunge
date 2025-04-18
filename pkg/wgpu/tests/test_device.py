from crunge import wgpu


def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    device = adapter.create_device()
    print(device)

if __name__ == "__main__":
    main()