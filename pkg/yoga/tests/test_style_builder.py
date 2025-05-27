from crunge import yoga


def main():
    style = (
        yoga.StyleBuilder()
        .flex_direction(yoga.FlexDirection.ROW)
        .align_items(yoga.Align.CENTER)
        .dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        .build()
    )
    print(f"Style: {style}")

if __name__ == "__main__":
    main()
