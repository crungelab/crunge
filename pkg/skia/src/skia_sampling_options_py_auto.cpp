#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkSamplingOptions.h>


namespace py = pybind11;

void init_skia_sampling_options_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkFilterMode>(_skia, "FilterMode", py::arithmetic())
        .value("K_NEAREST", SkFilterMode::kNearest)
        .value("K_LINEAR", SkFilterMode::kLinear)
        .value("K_LAST", SkFilterMode::kLast)
        .export_values()
    ;
    py::enum_<SkMipmapMode>(_skia, "MipmapMode", py::arithmetic())
        .value("K_NONE", SkMipmapMode::kNone)
        .value("K_NEAREST", SkMipmapMode::kNearest)
        .value("K_LINEAR", SkMipmapMode::kLinear)
        .value("K_LAST", SkMipmapMode::kLast)
        .export_values()
    ;
    py::class_<SkCubicResampler> _CubicResampler(_skia, "CubicResampler");
    registry.on(_skia, "CubicResampler", _CubicResampler);
        _CubicResampler
        .def_readwrite("b", &SkCubicResampler::B)
        .def_readwrite("c", &SkCubicResampler::C)
        .def_static("mitchell", &SkCubicResampler::Mitchell
            , py::return_value_policy::automatic_reference)
        .def_static("catmull_rom", &SkCubicResampler::CatmullRom
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<SkSamplingOptions> _SamplingOptions(_skia, "SamplingOptions");
    registry.on(_skia, "SamplingOptions", _SamplingOptions);
        _SamplingOptions
        .def_readonly("max_aniso", &SkSamplingOptions::maxAniso)
        .def_readonly("use_cubic", &SkSamplingOptions::useCubic)
        .def_readonly("cubic", &SkSamplingOptions::cubic)
        .def_readonly("filter", &SkSamplingOptions::filter)
        .def_readonly("mipmap", &SkSamplingOptions::mipmap)
        .def(py::init<>())
        .def(py::init<const SkSamplingOptions &>()
        , py::arg("")
        )
        .def(py::init<SkFilterMode, SkMipmapMode>()
        , py::arg("fm")
        , py::arg("mm")
        )
        .def(py::init<SkFilterMode>()
        , py::arg("fm")
        )
        .def(py::init<const SkCubicResampler &>()
        , py::arg("c")
        )
        .def_static("aniso", &SkSamplingOptions::Aniso
            , py::arg("max_aniso")
            , py::return_value_policy::automatic_reference)
        .def("is_aniso", &SkSamplingOptions::isAniso
            , py::return_value_policy::automatic_reference)
    ;


}