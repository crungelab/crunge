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
        .def_readwrite("f_image_provider", &skgpu::graphite::RecorderOptions::fImageProvider)
        .def_readwrite("f_gpu_budget_in_bytes", &skgpu::graphite::RecorderOptions::fGpuBudgetInBytes)
        .def_readwrite("f_require_ordered_recordings", &skgpu::graphite::RecorderOptions::fRequireOrderedRecordings)
    ;

    py::class_<skgpu::graphite::Recorder> _Recorder(_skia, "Recorder");
    registry.on(_skia, "Recorder", _Recorder);
        _Recorder
        .def("backend", &skgpu::graphite::Recorder::backend
            )
        .def("snap", &skgpu::graphite::Recorder::snap
            )
        .def("client_image_provider", py::overload_cast<>(&skgpu::graphite::Recorder::clientImageProvider)
            )
        .def("client_image_provider", py::overload_cast<>(&skgpu::graphite::Recorder::clientImageProvider, py::const_)
            )
        .def("max_texture_size", &skgpu::graphite::Recorder::maxTextureSize
            )
        .def("create_backend_texture", &skgpu::graphite::Recorder::createBackendTexture
            , py::arg("dimensions")
            , py::arg("arg1")
            )
        .def("update_backend_texture", &skgpu::graphite::Recorder::updateBackendTexture
            , py::arg("arg0")
            , py::arg("src_data")
            , py::arg("num_levels")
            , py::arg("arg3") = nullptr
            , py::arg("arg4") = nullptr
            )
        .def("update_compressed_backend_texture", &skgpu::graphite::Recorder::updateCompressedBackendTexture
            , py::arg("arg0")
            , py::arg("data")
            , py::arg("data_size")
            , py::arg("arg3") = nullptr
            , py::arg("arg4") = nullptr
            )
        .def("delete_backend_texture", &skgpu::graphite::Recorder::deleteBackendTexture
            , py::arg("arg0")
            )
        .def("add_finish_info", &skgpu::graphite::Recorder::addFinishInfo
            , py::arg("arg0")
            )
        .def("make_deferred_canvas", &skgpu::graphite::Recorder::makeDeferredCanvas
            , py::arg("arg0")
            , py::arg("arg1")
            )
        .def("free_gpu_resources", &skgpu::graphite::Recorder::freeGpuResources
            )
        .def("perform_deferred_cleanup", &skgpu::graphite::Recorder::performDeferredCleanup
            , py::arg("ms_not_used")
            )
        .def("current_budgeted_bytes", &skgpu::graphite::Recorder::currentBudgetedBytes
            )
        .def("current_purgeable_bytes", &skgpu::graphite::Recorder::currentPurgeableBytes
            )
        .def("max_budgeted_bytes", &skgpu::graphite::Recorder::maxBudgetedBytes
            )
        .def("set_max_budgeted_bytes", &skgpu::graphite::Recorder::setMaxBudgetedBytes
            , py::arg("bytes")
            )
        .def("dump_memory_statistics", &skgpu::graphite::Recorder::dumpMemoryStatistics
            , py::arg("trace_memory_dump")
            )
    ;


}