from crunge import yoga

def main():
    # Create a root node
    style = yoga.Style()
    print(f"Style: {style}")
    style.set_flex_direction(yoga.FlexDirection.ROW)
    style.set_align_items(yoga.Align.CENTER)
    style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
    print(f"Updated Style: {style}")

    root = yoga.Layout()
    root.set_style(style)

if __name__ == "__main__":
    main()