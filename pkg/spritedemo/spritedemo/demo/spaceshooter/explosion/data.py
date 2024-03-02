import numpy as np

vertex_data = np.array(
    [
        -0.5, -0.5, # Bottom left
        0.5, -0.5,  # Bottom right
        0.5, 0.5,   # Top right

        -0.5, 0.5,   # Top left
        0.5, 0.5,   # Top right
        -0.5, -0.5, # Bottom left
     ],
    dtype=np.float32,
)
