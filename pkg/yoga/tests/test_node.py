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
    root.calculate_layout(width=100, height=100)

    # Print the layout of the root and child nodes
    print(f"Root Node Layout: {root.get_layout()}")
    print(f"Child Node Layout: {child.get_layout()}")
    
if __name__ == "__main__":
    main()