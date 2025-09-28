#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkData.h>
#include <include/core/SkStream.h>


namespace py = pybind11;

void init_skia_data_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkData,sk_sp<SkData>> _Data(_skia, "Data");
    registry.on(_skia, "Data", _Data);
        _Data
        .def("size", &SkData::size
            , py::return_value_policy::automatic_reference)
        .def("is_empty", &SkData::isEmpty
            , py::return_value_policy::automatic_reference)
        .def("data", &SkData::data
            , py::return_value_policy::automatic_reference)
        .def("bytes", &SkData::bytes
            , py::return_value_policy::automatic_reference)
        .def("writable_data", &SkData::writable_data
            , py::return_value_policy::automatic_reference)
        .def("copy_range", &SkData::copyRange
            , py::arg("offset")
            , py::arg("length")
            , py::arg("buffer")
            , py::return_value_policy::automatic_reference)
        .def("equals", &SkData::equals
            , py::arg("other")
            , py::return_value_policy::automatic_reference)
        .def_static("make_with_copy", &SkData::MakeWithCopy
            , py::arg("data")
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_uninitialized", &SkData::MakeUninitialized
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_zero_initialized", &SkData::MakeZeroInitialized
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_with_c_string", &SkData::MakeWithCString
            , py::arg("cstr")
            , py::return_value_policy::automatic_reference)
        .def_static("make_with_proc", &SkData::MakeWithProc
            , py::arg("ptr")
            , py::arg("length")
            , py::arg("proc")
            , py::arg("ctx")
            , py::return_value_policy::automatic_reference)
        .def_static("make_without_copy", &SkData::MakeWithoutCopy
            , py::arg("data")
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_malloc", &SkData::MakeFromMalloc
            , py::arg("data")
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_file_name", &SkData::MakeFromFileName
            , py::arg("path")
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_file", &SkData::MakeFromFILE
            , py::arg("f")
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_fd", &SkData::MakeFromFD
            , py::arg("fd")
            , py::return_value_policy::automatic_reference)
        .def_static("make_from_stream", &SkData::MakeFromStream
            , py::arg("")
            , py::arg("size")
            , py::return_value_policy::automatic_reference)
        .def_static("make_subset", &SkData::MakeSubset
            , py::arg("src")
            , py::arg("offset")
            , py::arg("length")
            , py::return_value_policy::automatic_reference)
        .def_static("make_empty", &SkData::MakeEmpty
            , py::return_value_policy::automatic_reference)
    ;


}