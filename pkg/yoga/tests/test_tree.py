import math

from crunge import yoga

def main():
    # Create a root node
    root_style = yoga.Style()

    root_style.set_flex_direction(yoga.FlexDirection.ROW)
    #root_style.set_align_items(yoga.Align.CENTER)
    root_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
    #style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(math.nan))
    root_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(100))
    #style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(math.nan))

    root = yoga.Node()
    root.set_style(root_style)

    child0 = yoga.Node()
    child0_style = yoga.Style()
    child0_style.set_flex_grow(1.0)
    child0_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
    child0_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(20))
    child0_style.set_margin(yoga.Edge.RIGHT, yoga.StyleLength.points(10))

    child0.set_style(child0_style)

    root.add_child(child0)

    child1 = yoga.Node()
    child1.set_owner(root)
    child1_style = yoga.Style()
    child1_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
    child1_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(10))
    child1_style.set_flex_grow(1.0)

    child1.set_style(child1_style)
    
    root.add_child(child1)

    # Calculate layout for the root node
    #root.calculate_layout(width=100, height=100)
    yoga.calculate_layout(root, 100, 100, yoga.Direction.LTR)
    #yoga.calculate_layout(root, math.nan, math.nan, yoga.Direction.LTR)

    child0_layout = child0.get_layout()
    child0_left = child0_layout.position(yoga.PhysicalEdge.LEFT)
    child0_top = child0_layout.position(yoga.PhysicalEdge.TOP)
    child0_width = child0_layout.dimension(yoga.Dimension.WIDTH)
    child0_height = child0_layout.dimension(yoga.Dimension.HEIGHT)

    print(f"Child 0 Layout: Left={child0_left}, Top={child0_top}, Width={child0_width}, Height={child0_height}")

    child1_layout = child1.get_layout()
    child1_left = child1_layout.position(yoga.PhysicalEdge.LEFT)
    child1_top = child1_layout.position(yoga.PhysicalEdge.TOP)
    child1_width = child1_layout.dimension(yoga.Dimension.WIDTH)
    child1_height = child1_layout.dimension(yoga.Dimension.HEIGHT)

    print(f"Child 1 Layout: Left={child1_left}, Top={child1_top}, Width={child1_width}, Height={child1_height}")

    for node in root.get_children():
        layout = node.get_layout()
        left = layout.position(yoga.PhysicalEdge.LEFT)
        top = layout.position(yoga.PhysicalEdge.TOP)
        width = layout.dimension(yoga.Dimension.WIDTH)
        height = layout.dimension(yoga.Dimension.HEIGHT)
        print(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")

if __name__ == "__main__":
    main()