import numpy as np
import glm

def compute_tangents(indices, vertices, uvs, normals):
    tangents = np.zeros((len(vertices), 4), dtype=np.float32)

    for i in range(0, len(indices), 3):
        i0, i1, i2 = indices[i], indices[i + 1], indices[i + 2]

        v0, v1, v2 = glm.vec3(*vertices[i0]), glm.vec3(*vertices[i1]), glm.vec3(*vertices[i2])
        uv0, uv1, uv2 = glm.vec2(*uvs[i0]), glm.vec2(*uvs[i1]), glm.vec2(*uvs[i2])

        deltaPos1, deltaPos2 = v1 - v0, v2 - v0
        deltaUV1, deltaUV2 = uv1 - uv0, uv2 - uv0

        det = deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x

        # Check for zero determinant and skip if necessary
        if np.abs(det) < 1e-8:
            continue

        r = 1.0 / det
        tangent = (deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y) * r
        bitangent = (deltaPos2 * deltaUV1.x - deltaPos1 * deltaUV2.x) * r

        # Determine handedness
        handedness = 1.0 if glm.dot(glm.cross(glm.vec3(*normals[i0]), tangent), bitangent) > 0.0 else -1.0

        # Accumulate tangents
        for i in [i0, i1, i2]:
            tangents[i, :3] += np.array([tangent.x, tangent.y, tangent.z])
            tangents[i, 3] = handedness

    # Normalize tangents
    for i in range(len(tangents)):
        tangents[i, :3] = glm.normalize(glm.vec3(*tangents[i, :3])).xyz

    return tangents

'''
import numpy as np
import glm

def compute_tangents(vertices, uvs, normals, indices):
    tangents = np.zeros((len(vertices), 4), dtype=np.float32)

    for i in range(0, len(indices), 3):
        i0, i1, i2 = indices[i], indices[i + 1], indices[i + 2]

        v0, v1, v2 = glm.vec3(*vertices[i0]), glm.vec3(*vertices[i1]), glm.vec3(*vertices[i2])
        uv0, uv1, uv2 = glm.vec2(*uvs[i0]), glm.vec2(*uvs[i1]), glm.vec2(*uvs[i2])

        deltaPos1, deltaPos2 = v1 - v0, v2 - v0
        deltaUV1, deltaUV2 = uv1 - uv0, uv2 - uv0

        r = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x)
        tangent = (deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y) * r
        bitangent = (deltaPos2 * deltaUV1.x - deltaPos1 * deltaUV2.x) * r

        # Determine handedness
        handedness = 1.0 if glm.dot(glm.cross(glm.vec3(*normals[i0]), tangent), bitangent) > 0.0 else -1.0

        # Accumulate tangents
        for i in [i0, i1, i2]:
            tangents[i, :3] += np.array([tangent.x, tangent.y, tangent.z])
            tangents[i, 3] = handedness

    # Normalize tangents
    for i in range(len(tangents)):
        tangents[i, :3] = glm.normalize(glm.vec3(*tangents[i, :3])).xyz

    return tangents
'''

'''
# Your model's data
vertices = [...]  # Replace with your vertices
uvs = [...]       # Replace with your UVs
normals = [...]   # Replace with your normals
indices = [...]   # Replace with your indices

# Calculate tangents with handedness
tangents = calculate_tangents_with_handedness(vertices, uvs, normals, indices)
'''