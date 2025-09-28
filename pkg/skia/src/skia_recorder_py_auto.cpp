#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/gpu/graphite/Recorder.h>
#include <include/gpu/graphite/ImageProvider.h>
#include <include/gpu/graphite/BackendTexture.h>

#include <include/core/SkPixmap.h>
#include <include/core/SkTraceMemoryDump.h>
#include <include/core/SkCanvas.h>


namespace py = pybind11;

void init_skia_recorder_py_auto(py::module &_skia, Registry &registry) {
    py::class_<skgpu::graphite::RecorderOptions> _RecorderOptions(_skia, "RecorderOptions");
    registry.on(_skia, "RecorderOptions", _RecorderOptions);
        _RecorderOptions
        .def(py::init<>())
        .def(py::init<const skgpu::graphite::RecorderOptions &>()
        , py::arg("")
        )
        .def_readwrite("f_image_provider", &skgpu::graphite::RecorderOptions::fImageProvider)
        .def_readwrite("f_gpu_budget_in_bytes", &skgpu::graphite::RecorderOptions::fGpuBudgetInBytes)
        .def_readwrite("f_require_ordered_recordings", &skgpu::graphite::RecorderOptions::fRequireOrderedRecordings)
    ;

    py::class_<skgpu::graphite::Recorder> _Recorder(_skia, "Recorder");
    registry.on(_skia, "Recorder", _Recorder);
        _Recorder
        .def("backend", &skgpu::graphite::Recorder::backend
            , py::return_value_policy::automatic_reference)
        .def("snap", &skgpu::graphite::Recorder::snap
            , py::return_value_policy::automatic_reference)
        .def("client_image_provider", py::overload_cast<>(&skgpu::graphite::Recorder::clientImageProvider)
            , py::return_value_policy::automatic_reference)
        .def("client_image_provider", py::overload_cast<>(&skgpu::graphite::Recorder::clientImageProvider, py::const_)
            , py::return_value_policy::automatic_reference)
        .def("max_texture_size", &skgpu::graphite::Recorder::maxTextureSize
            , py::return_value_policy::automatic_reference)
        .def("create_backend_texture", &skgpu::graphite::Recorder::createBackendTexture
            , py::arg("dimensions")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("update_backend_texture", &skgpu::graphite::Recorder::updateBackendTexture
            , py::arg("")
            , py::arg("src_data")
            , py::arg("num_levels")
            , py::arg("") = nullptr
            , py::arg("") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("update_compressed_backend_texture", &skgpu::graphite::Recorder::updateCompressedBackendTexture
            , py::arg("")
            , py::arg("data")
            , py::arg("data_size")
            , py::arg("") = nullptr
            , py::arg("") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("delete_backend_texture", &skgpu::graphite::Recorder::deleteBackendTexture
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("add_finish_info", &skgpu::graphite::Recorder::addFinishInfo
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("make_deferred_canvas", &skgpu::graphite::Recorder::makeDeferredCanvas
            , py::arg("")
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("free_gpu_resources", &skgpu::graphite::Recorder::freeGpuResources
            , py::return_value_policy::automatic_reference)
        .def("perform_deferred_cleanup", &skgpu::graphite::Recorder::performDeferredCleanup
            , py::arg("ms_not_used")
            , py::return_value_policy::automatic_reference)
        .def("current_budgeted_bytes", &skgpu::graphite::Recorder::currentBudgetedBytes
            , py::return_value_policy::automatic_reference)
        .def("current_purgeable_bytes", &skgpu::graphite::Recorder::currentPurgeableBytes
            , py::return_value_policy::automatic_reference)
        .def("max_budgeted_bytes", &skgpu::graphite::Recorder::maxBudgetedBytes
            , py::return_value_policy::automatic_reference)
        .def("set_max_budgeted_bytes", &skgpu::graphite::Recorder::setMaxBudgetedBytes
            , py::arg("bytes")
            , py::return_value_policy::automatic_reference)
        .def("dump_memory_statistics", &skgpu::graphite::Recorder::dumpMemoryStatistics
            , py::arg("trace_memory_dump")
            , py::return_value_policy::automatic_reference)
    ;


}