import numpy as np

vertex_data = np.array(
    [
        -0.5, -0.5, 1.0, 0.0, 0.0, # Bottom left
        0.5, -0.5, 0.0, 1.0, 0.0,  # Bottom right
        0.5, 0.5, 0.0, 0.0, 1.0,   # Top right

        -0.5, 0.5, 1.0, 1.0, 1.0,   # Top left
        0.5, 0.5, 0.0, 0.0, 1.0,   # Top right
        -0.5, -0.5, 1.0, 0.0, 0.0, # Bottom left

     ],
    dtype=np.float32,
)
