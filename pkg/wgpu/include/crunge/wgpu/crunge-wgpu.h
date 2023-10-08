#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include <dawn/webgpu_cpp.h>

namespace py = pybind11;

namespace wgpu {
    typedef std::vector<BindGroupLayoutEntry> BindGroupLayoutEntries;
    typedef std::vector<BindGroupEntry> BindGroupEntries;
    typedef std::vector<VertexAttribute> VertexAttributes;
}

PYBIND11_MAKE_OPAQUE(wgpu::BindGroupLayoutEntries)
PYBIND11_MAKE_OPAQUE(wgpu::BindGroupEntries)
PYBIND11_MAKE_OPAQUE(wgpu::VertexAttributes)
