from crunge import yoga

def main():
    # Create a root node
    root = yoga.Layout()

    # Set the width and height of the root node
    root.set_width(100)
    root.set_height(100)

    # Create a child node
    child = yoga.Layout()

    # Set the width and height of the child node
    child.set_width(50)
    child.set_height(50)

    # Add the child node to the root node
    root.insert_child(child, 0)

    # Calculate layout for the root node
    root.calculate_bounds(width=100, height=100, direction=yoga.Direction.LTR)

    # Print the layout of the root and child nodes
    root_bounds = root.get_computed_bounds()
    child_bounds = child.get_computed_bounds()
    #print(f"Root Node Layout: {root_layout}")
    print(f"Root Node Bounds: left={root_bounds.left}, top={root_bounds.top}, width={root_bounds.width}, height={root_bounds.height}")
    print(f"Child Node Bounds: left={child_bounds.left}, top={child_bounds.top}, width={child_bounds.width}, height={child_bounds.height}")

if __name__ == "__main__":
    main()