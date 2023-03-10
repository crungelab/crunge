#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <crunge/core/bindtools.h>

#include <crunge/bgfx/crunge-bgfx.h>
#include <bx/allocator.h>

using namespace bgfx;

namespace py = pybind11;

void init_platform(py::module &_bgfx, Registry &registry) {
        py::enum_<bgfx::RenderFrame::Enum>(_bgfx, "RenderFrame", py::arithmetic())
            .value("NO_CONTEXT", bgfx::RenderFrame::Enum::NoContext)
            .value("RENDER", bgfx::RenderFrame::Enum::Render)
            .value("TIMEOUT", bgfx::RenderFrame::Enum::Timeout)
            .value("EXITING", bgfx::RenderFrame::Enum::Exiting)
            .value("COUNT", bgfx::RenderFrame::Enum::Count)
            .export_values();

    _bgfx.def("render_frame", &bgfx::renderFrame
    , py::arg("_msecs") = -1
    , py::return_value_policy::automatic_reference);

    _bgfx.def("set_platform_data", &bgfx::setPlatformData
    , py::arg("_data")
    , py::return_value_policy::automatic_reference);

    PYCLASS_BEGIN(_bgfx, bgfx::InternalData, InternalData)
        InternalData.def_readwrite("caps", &bgfx::InternalData::caps);
        InternalData.def_readwrite("context", &bgfx::InternalData::context);
    PYCLASS_END(_bgfx, bgfx::InternalData, InternalData)

    _bgfx.def("get_internal_data", &bgfx::getInternalData
    , py::return_value_policy::automatic_reference);

    _bgfx.def("override_internal", py::overload_cast<bgfx::TextureHandle, uintptr_t>(&bgfx::overrideInternal)
    , py::arg("_handle")
    , py::arg("_ptr")
    , py::return_value_policy::automatic_reference);

    _bgfx.def("override_internal", py::overload_cast<bgfx::TextureHandle, uint16_t, uint16_t, uint8_t, TextureFormat::Enum, uint64_t>(&bgfx::overrideInternal)
    , py::arg("_handle")
    , py::arg("_width")
    , py::arg("_height")
    , py::arg("_num_mips")
    , py::arg("_format")
    , py::arg("_flags") = BGFX_TEXTURE_NONE|BGFX_SAMPLER_NONE
    , py::return_value_policy::automatic_reference);


}