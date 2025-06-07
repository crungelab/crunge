#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <tiny_gltf.h>

#include <cxbind/cxbind.h>

#include <crunge/gltf/crunge-gltf.h>
#include <crunge/gltf/conversions.h>

#include "mikktspace/mikktspace.h"

namespace py = pybind11;

struct MeshData {
    float* positions;
    float* normals;
    float* texcoords;
    int* indices;
    float* tangents;
    int num_vertices;
    int num_faces;
};

int get_num_faces(const SMikkTSpaceContext* ctx) {
    return static_cast<MeshData*>(ctx->m_pUserData)->num_faces;
}

int get_num_verts_of_face(const SMikkTSpaceContext*, int /*face*/) { return 3; }

void get_position(const SMikkTSpaceContext* ctx, float pos[3], int face, int vert) {
    MeshData* data = (MeshData*)ctx->m_pUserData;
    int idx = data->indices[face * 3 + vert];
    std::copy(data->positions + idx * 3, data->positions + idx * 3 + 3, pos);
}

void get_normal(const SMikkTSpaceContext* ctx, float norm[3], int face, int vert) {
    MeshData* data = (MeshData*)ctx->m_pUserData;
    int idx = data->indices[face * 3 + vert];
    std::copy(data->normals + idx * 3, data->normals + idx * 3 + 3, norm);
}

void get_texcoord(const SMikkTSpaceContext* ctx, float uv[2], int face, int vert) {
    MeshData* data = (MeshData*)ctx->m_pUserData;
    int idx = data->indices[face * 3 + vert];
    std::copy(data->texcoords + idx * 2, data->texcoords + idx * 2 + 2, uv);
}

void set_tangent(const SMikkTSpaceContext* ctx, const float tangent[3], float fSign, int face, int vert) {
    MeshData* data = (MeshData*)ctx->m_pUserData;
    int idx = data->indices[face * 3 + vert];
    float* t = data->tangents + idx * 4;
    t[0] = tangent[0];
    t[1] = tangent[1];
    t[2] = tangent[2];
    t[3] = fSign;
}

py::array_t<float> compute_tangents(
    py::array_t<int, py::array::c_style | py::array::forcecast> indices,
    py::array_t<float, py::array::c_style | py::array::forcecast> vertices,
    py::array_t<float, py::array::c_style | py::array::forcecast> uvs,
    py::array_t<float, py::array::c_style | py::array::forcecast> normals
) {
    // Buffer info
    auto idx = indices.request();
    auto vtx = vertices.request();
    auto uv = uvs.request();
    auto nrm = normals.request();

    int num_vertices = vtx.shape[0];
    int num_faces = idx.size / 3;

    // Output tangents array
    py::array_t<float> tangents({num_vertices, 4});
    auto tan = tangents.request();

    MeshData mesh {
        static_cast<float*>(vtx.ptr),
        static_cast<float*>(nrm.ptr),
        static_cast<float*>(uv.ptr),
        static_cast<int*>(idx.ptr),
        static_cast<float*>(tan.ptr),
        num_vertices,
        num_faces
    };

    // Set up Mikktspace interface
    SMikkTSpaceInterface iface = {};
    iface.m_getNumFaces = get_num_faces;
    iface.m_getNumVerticesOfFace = get_num_verts_of_face;
    iface.m_getPosition = get_position;
    iface.m_getNormal = get_normal;
    iface.m_getTexCoord = get_texcoord;
    iface.m_setTSpaceBasic = set_tangent;

    SMikkTSpaceContext context = {};
    context.m_pInterface = &iface;
    context.m_pUserData = &mesh;

    genTangSpaceDefault(&context);

    return tangents;
}

void init_mikktspace_py(py::module &_gltf, Registry &registry) {
    _gltf.def("compute_tangents", &compute_tangents,
        py::arg("indices"),
        py::arg("vertices"),
        py::arg("uvs"),
        py::arg("normals"),
        "Compute tangent vectors (returns new numpy array, shape (V,4))"
    );
}
