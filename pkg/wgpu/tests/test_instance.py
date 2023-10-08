from crunge import wgpu


def main():
    instance = wgpu.create_instance()
    print(instance)

if __name__ == "__main__":
    main()