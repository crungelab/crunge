from crunge import yoga

def main():
    # Create a root node
    root = yoga.Node()

    # Set the width and height of the root node
    root.set_width(100)
    root.set_height(100)

    # Create a child node
    child = yoga.Node()

    # Set the width and height of the child node
    child.set_width(50)
    child.set_height(50)

    # Add the child node to the root node
    root.insert_child(child, 0)

    # Calculate layout for the root node
    root.calculate_layout(width=100, height=100, direction=yoga.Direction.LTR)

    # Print the layout of the root and child nodes
    root_layout = root.get_computed_layout()
    child_layout = child.get_computed_layout()
    #print(f"Root Node Layout: {root_layout}")
    print(f"Root Node Layout: left={root_layout.left}, top={root_layout.top}, width={root_layout.width}, height={root_layout.height}")
    print(f"Child Node Layout: left={child_layout.left}, top={child_layout.top}, width={child_layout.width}, height={child_layout.height}")

if __name__ == "__main__":
    main()