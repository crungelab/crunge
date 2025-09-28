#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkImageFilter.h>
#include <include/core/SkSerialProcs.h>
#include <include/core/SkMatrix.h>
#include <include/core/SkColorFilter.h>

namespace py = pybind11;

void init_skia_image_filter_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkImageFilter,sk_sp<SkImageFilter>> _ImageFilter(_skia, "ImageFilter");
    registry.on(_skia, "ImageFilter", _ImageFilter);
        py::enum_<SkImageFilter::MapDirection>(_ImageFilter, "MapDirection", py::arithmetic())
            .value("K_FORWARD_MAP_DIRECTION", SkImageFilter::MapDirection::kForward_MapDirection)
            .value("K_REVERSE_MAP_DIRECTION", SkImageFilter::MapDirection::kReverse_MapDirection)
            .export_values()
        ;
        _ImageFilter
        .def("filter_bounds", &SkImageFilter::filterBounds
            , py::arg("src")
            , py::arg("ctm")
            , py::arg("")
            , py::arg("input_rect") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("count_inputs", &SkImageFilter::countInputs
            , py::return_value_policy::automatic_reference)
        .def("get_input", &SkImageFilter::getInput
            , py::arg("i")
            , py::return_value_policy::automatic_reference)
        .def("compute_fast_bounds", &SkImageFilter::computeFastBounds
            , py::arg("bounds")
            , py::return_value_policy::automatic_reference)
        .def("can_compute_fast_bounds", &SkImageFilter::canComputeFastBounds
            , py::return_value_policy::automatic_reference)
        .def("make_with_local_matrix", &SkImageFilter::makeWithLocalMatrix
            , py::arg("matrix")
            , py::return_value_policy::automatic_reference)
        .def_static("deserialize", &SkImageFilter::Deserialize
            , py::arg("data")
            , py::arg("size")
            , py::arg("procs") = nullptr
            , py::return_value_policy::automatic_reference)
    ;


}