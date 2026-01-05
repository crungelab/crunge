from crunge import wgpu

def main():
    color = wgpu.Color(r=1, g=1, b=1, a=1)
    print(color.r)
    print(color.g)
    print(color.b)
    print(color.a)

if __name__ == "__main__":
    main()
