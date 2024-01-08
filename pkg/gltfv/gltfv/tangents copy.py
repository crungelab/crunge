import numpy as np
import glm

def calculate_tangents_bitangents(vertices, uvs, normals, indices):
    tangents = np.zeros_like(vertices)
    bitangents = np.zeros_like(vertices)

    # Iterate through each triangle
    for i in range(0, len(indices), 3):
        # Get the indices of the triangle
        i0 = indices[i]
        i1 = indices[i + 1]
        i2 = indices[i + 2]

        # Vertices
        v0 = glm.vec3(*vertices[i0])
        v1 = glm.vec3(*vertices[i1])
        v2 = glm.vec3(*vertices[i2])

        # UVs
        uv0 = glm.vec2(*uvs[i0])
        uv1 = glm.vec2(*uvs[i1])
        uv2 = glm.vec2(*uvs[i2])

        # Edges and delta UVs
        deltaPos1 = v1 - v0
        deltaPos2 = v2 - v0
        deltaUV1 = uv1 - uv0
        deltaUV2 = uv2 - uv0

        # Calculate the tangent and the bitangent
        r = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x)
        tangent = (deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y) * r
        bitangent = (deltaPos2 * deltaUV1.x - deltaPos1 * deltaUV2.x) * r

        # Accumulate the tangents and bitangents for each vertex of the triangle
        for i in [i0, i1, i2]:
            tangents[i] += glm.normalize(tangent)
            bitangents[i] += glm.normalize(bitangent)

    # Normalize and orthogonalize the accumulated tangents and bitangents
    for i in range(len(vertices)):
        # Grab the normal for this vertex
        n = glm.vec3(*normals[i])

        # Orthogonalize and normalize the tangent so it's perpendicular to the normal
        tangents[i] = glm.normalize(tangents[i] - n * glm.dot(n, tangents[i]))

        # Calculate the bitangent from the cross product of the normal and the tangent
        bitangents[i] = glm.cross(n, tangents[i])

    return tangents, bitangents

'''
# Your model's data
vertices = [...]  # Replace with your vertices
uvs = [...]       # Replace with your UVs
normals = [...]   # Replace with your normals
indices = [...]   # Replace with your indices

# Calculate tangents and bitangents
tangents, bitangents = calculate_tangents_bitangents(vertices, uvs, normals, indices)
'''