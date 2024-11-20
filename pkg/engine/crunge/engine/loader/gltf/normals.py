import numpy as np
import glm

def compute_normals(indices, vertices):
    # Ensure vertices is a numpy array
    #vertices = np.array(vertices, dtype=np.float32)

    # Initialize normals array with zeros
    normals = np.zeros(vertices.shape, dtype=np.float32)

    # Iterate over the indices in steps of 3 (assuming triangles)
    for i in range(0, len(indices), 3):
        # Get the vertex indices for the current triangle
        i1, i2, i3 = indices[i], indices[i + 1], indices[i + 2]

        # Get the vertices for the current triangle
        v1 = glm.vec3(*vertices[i1])
        v2 = glm.vec3(*vertices[i2])
        v3 = glm.vec3(*vertices[i3])

        # Compute the normal for the current triangle
        edge1 = v2 - v1
        edge2 = v3 - v1
        normal = glm.normalize(glm.cross(edge1, edge2))

        # Add the normal to each vertex of the triangle
        normals[i1] += normal
        normals[i2] += normal
        normals[i3] += normal

    # Normalize the normals
    for i in range(len(normals)):
        normals[i] = glm.normalize(glm.vec3(*normals[i]))

    return normals
