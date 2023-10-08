from crunge import wgpu

def main():
    color = wgpu.Color(1, 1, 1, 1)
    print(color.r)
    print(color.g)
    print(color.b)
    print(color.a)

if __name__ == "__main__":
    main()
