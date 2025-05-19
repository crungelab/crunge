#include <limits>
#include <filesystem>
#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>
#include <pybind11/numpy.h>

//#include <dawn/webgpu_cpp.h>
// #include <wgpu.h>
#include <dawn/native/DawnNative.h>
#include <dawn/dawn_proc.h>

#include <cxbind/cxbind.h>

#include <crunge/wgpu/pywgpu.h>
#include <crunge/wgpu/crunge-wgpu.h>
#include <crunge/wgpu/conversions.h>

//#include "callbacks.h"


using namespace crunge_wgpu;

namespace py = pybind11;

using namespace pywgpu;

WGPU_IMPORT_BITMASK_OPERATORS

void CreateProcTable()
{
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);
}

PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::BindGroupLayout>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::BindGroupLayoutEntry>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::BindGroupEntry>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::VertexAttribute>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::ColorTargetState>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::VertexBufferLayout>)
PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::RenderPassColorAttachment>)

//PYBIND11_MAKE_OPAQUE(std::vector<pywgpu::FutureWaitInfo>)

void init_wgpu_py(py::module &_wgpu, Registry &registry)
{
    _wgpu.def("create_proc_table", &CreateProcTable);

    py::bind_vector<std::vector<pywgpu::BindGroupLayout>>(_wgpu, "BindGroupLayouts", "BindGroupLayout Vector");
    py::bind_vector<std::vector<pywgpu::BindGroupLayoutEntry>>(_wgpu, "BindGroupLayoutEntries", "BindGroupLayoutEntry Vector");
    py::bind_vector<std::vector<pywgpu::BindGroupEntry>>(_wgpu, "BindGroupEntries", "BindGroupEntry Vector");
    py::bind_vector<std::vector<pywgpu::VertexAttribute>>(_wgpu, "VertexAttributes", "VertexAttribute Vector");
    py::bind_vector<std::vector<pywgpu::ColorTargetState>>(_wgpu, "ColorTargetStates", "ColorTargetState Vector");
    py::bind_vector<std::vector<pywgpu::VertexBufferLayout>>(_wgpu, "VertexBufferLayouts", "VertexBufferLayout Vector");
    py::bind_vector<std::vector<pywgpu::RenderPassColorAttachment>>(_wgpu, "RenderPassColorAttachments", "RenderPassColorAttachment Vector");

    //py::bind_vector<std::vector<pywgpu::FutureWaitInfo>>(_wgpu, "FutureWaitInfos", "FutureWaitInfo Vector");


    PYEXTEND_BEGIN(pywgpu::Instance, Instance)
    Instance.def("wait_any",
        [] (pywgpu::Instance &self,
            std::vector<pywgpu::FutureWaitInfo> &futures,
            uint64_t timeout) 
        {
            py::scoped_ostream_redirect stream(
                std::cerr,                                // std::ostream&
                py::module_::import("sys").attr("stderr") // Python output
                );
    
            // pybind11 has already made you a contiguous vector<FutureWaitInfo>
            self.WaitAny(
                static_cast<uint32_t>(futures.size()),
                futures.data(),
                timeout
            );
        },
        py::arg("futures"),
        py::arg("timeout") = UINT64_MAX
   );
    PYEXTEND_END

    PYEXTEND_BEGIN(pywgpu::Device, Device)
    Device.def_property_readonly("queue", [](const pywgpu::Device &self)
                                 { return self.GetQueue(); }, py::return_value_policy::automatic_reference);
    PYEXTEND_END

    PYEXTEND_BEGIN(pywgpu::Extent3D, Extent3D)
    Extent3D.def(py::init<uint32_t, uint32_t, uint32_t>(), py::arg("width"), py::arg("height") = 1, py::arg("depth") = 1);
    PYEXTEND_END

    PYEXTEND_BEGIN(pywgpu::Origin3D, Origin3D)
    Origin3D.def(py::init<uint32_t, uint32_t, uint32_t>(), py::arg("x"), py::arg("y"), py::arg("z"));
    PYEXTEND_END

    PYEXTEND_BEGIN(pywgpu::Color, Color)
    Color.def(py::init<float, float, float, float>(), py::arg("r"), py::arg("g"), py::arg("b"), py::arg("a"));
    PYEXTEND_END

    // TODO: Getting incompatible argument types when both signatures match.  Makes no sense ...
    // Fixed:  Turns out that py::buffer is not optional, but std::optional<py::buffer> is.

    /*
    TypeError: set_bind_group(): incompatible function arguments. The following argument types are supported:
        1. (self: crunge.wgpu._wgpu.ComputePassEncoder, group_index: int, group: crunge.wgpu._wgpu.BindGroup, dynamic_offset_count: int = 0, dynamic_offsets: int = None) -> None

    Invoked with: <crunge.wgpu._wgpu.ComputePassEncoder object at 0x7f7a6a76a8f0>, 0, <crunge.wgpu._wgpu.BindGroup object at 0x7f7a6a77c230>
    */

    // void RenderPassEncoder::SetBindGroup(uint32_t groupIndex, BindGroup const& group, uint32_t dynamicOffsetCount, uint32_t const * dynamicOffsets) const {

    /*
    PYEXTEND_BEGIN(pywgpu::RenderPassEncoder, RenderPassEncoder)
    RenderPassEncoder.def("set_bind_group", [](pywgpu::RenderPassEncoder &self, uint32_t groupIndex, BindGroup const &group)
                          { self.SetBindGroup(groupIndex, group, 0, nullptr); }, py::arg("group_index"), py::arg("group")
                          //, py::arg("dynamic_offset_count") = 0
                          //, py::arg("dynamic_offsets") = nullptr
                          ,
                          py::return_value_policy::automatic_reference);
    PYEXTEND_END

    PYEXTEND_BEGIN(pywgpu::ComputePassEncoder, ComputePassEncoder)
    ComputePassEncoder.def("set_bind_group", [](pywgpu::ComputePassEncoder &self, uint32_t groupIndex, BindGroup const &group)
                           { self.SetBindGroup(groupIndex, group, 0, nullptr); }, py::arg("group_index"), py::arg("group")
                           //, py::arg("dynamic_offset_count") = 0
                           //, py::arg("dynamic_offsets") = nullptr
                           ,
                           py::return_value_policy::automatic_reference);
    PYEXTEND_END
    */

    /*
    void Queue::WriteTexture (TexelCopyTextureInfo const* destination, void const* data, size_t dataSize, TexelCopyBufferLayout const* dataLayout, Extent3D const* writeSize) const {
        wgpuQueueWriteTexture(Get(), reinterpret_cast<WGPUTexelCopyTextureInfo const* >(destination), data, dataSize, reinterpret_cast<WGPUTexelCopyBufferLayout const* >(dataLayout), reinterpret_cast<WGPUExtent3D const* >(writeSize));    
    }
    */

    /*
    PYEXTEND_BEGIN(pywgpu::Queue, Queue)
    Queue.def("write_texture",
        [](pywgpu::Queue& self,
           const pywgpu::TexelCopyTextureInfo& destination,
           py::buffer buffer,
           const pywgpu::TexelCopyBufferLayout& layout,
           const pywgpu::Extent3D& write_size) {

            // Get buffer info
            py::buffer_info info = buffer.request();

            // Call the actual method
            self.WriteTexture(&destination, info.ptr, info.size * info.itemsize, &layout, &write_size);
        },
        py::arg("destination"),
        py::arg("data"),
        py::arg("layout"),
        py::arg("write_size"));

    Queue.def("write_texture_array",
        [](pywgpu::Queue& self,
            const pywgpu::TexelCopyTextureInfo& destination,
            //py::array_t<uint8_t, py::array::c_style | py::array::forcecast>  &buffer,
            py::array_t<uint8_t>  &buffer,
            const pywgpu::TexelCopyBufferLayout& layout,
            const pywgpu::Extent3D& write_size) {

            // Get buffer info
            py::buffer_info info = buffer.request();
    
            // Call the actual method
            self.WriteTexture(&destination, info.ptr, info.size * info.itemsize, &layout, &write_size);
        },
        py::arg("destination"),
        py::arg("data"),
        py::arg("layout"),
        py::arg("write_size"));

    */

    /*
    void Queue::WriteBuffer (Buffer buffer, uint64_t bufferOffset, void const* data, size_t size) const {
        wgpuQueueWriteBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), bufferOffset, data, size);    
    }
    .def("write_buffer", &pywgpu::Queue::WriteBuffer
        , py::arg("buffer"), py::arg("buffer_offset"), py::arg("data"), py::arg("size")
        , py::return_value_policy::automatic_reference)
    */

    /*
    Queue.def("write_buffer",
        [](pywgpu::Queue& self,
                pywgpu::Buffer& buffer,
            uint64_t bufferOffset,
            py::buffer data) {

            // Get buffer info
            py::buffer_info info = data.request();

            // Call the actual method
            self.WriteBuffer(buffer, bufferOffset, info.ptr, info.size * info.itemsize);
        },
        py::arg("buffer"),
        py::arg("buffer_offset"),
        py::arg("data")
        );
        
    Queue.def("write_buffer_array",
        [](pywgpu::Queue& self,
            pywgpu::Buffer& buffer,
            uint64_t bufferOffset,
            //py::array_t<uint8_t, py::array::c_style | py::array::forcecast>  &buffer,
            py::array_t<uint8_t>  &data) {

            // Get buffer info
            py::buffer_info info = data.request();
    
            // Call the actual method
            self.WriteBuffer(buffer, bufferOffset, info.ptr, info.size * info.itemsize);
        },
        py::arg("buffer"),
        py::arg("buffer_offset"),
        py::arg("data")
    );
            
    PYEXTEND_END
    */

}
