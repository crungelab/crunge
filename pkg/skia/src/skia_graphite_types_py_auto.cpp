#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/gpu/graphite/GraphiteTypes.h>
#include <include/gpu/graphite/BackendSemaphore.h>
#include <include/gpu/graphite/Recording.h>
#include <include/core/SkSurface.h>
#include <include/gpu/MutableTextureState.h>

namespace py = pybind11;

void init_skia_graphite_types_py_auto(py::module &_skia, Registry &registry) {
    py::class_<skgpu::graphite::InsertStatus> _InsertStatus(_skia, "InsertStatus");
    registry.on(_skia, "InsertStatus", _InsertStatus);
        py::enum_<skgpu::graphite::InsertStatus::V>(_InsertStatus, "V", py::arithmetic())
            .value("K_SUCCESS", skgpu::graphite::InsertStatus::V::kSuccess)
            .value("K_INVALID_RECORDING", skgpu::graphite::InsertStatus::V::kInvalidRecording)
            .value("K_PROMISE_IMAGE_INSTANTIATION_FAILED", skgpu::graphite::InsertStatus::V::kPromiseImageInstantiationFailed)
            .value("K_ADD_COMMANDS_FAILED", skgpu::graphite::InsertStatus::V::kAddCommandsFailed)
            .value("K_ASYNC_SHADER_COMPILES_FAILED", skgpu::graphite::InsertStatus::V::kAsyncShaderCompilesFailed)
            .value("K_OUT_OF_ORDER_RECORDING", skgpu::graphite::InsertStatus::V::kOutOfOrderRecording)
            .export_values()
        ;
        _InsertStatus
        .def(py::init<>())
        .def(py::init<skgpu::graphite::InsertStatus::V>()
        , py::arg("v")
        )
        .def(py::init<skgpu::graphite::InsertStatus::V, std::string>()
        , py::arg("v")
        , py::arg("message")
        )
        .def("message", &skgpu::graphite::InsertStatus::message
            )
    ;

    py::class_<skgpu::graphite::InsertRecordingInfo> _InsertRecordingInfo(_skia, "InsertRecordingInfo");
    registry.on(_skia, "InsertRecordingInfo", _InsertRecordingInfo);
        _InsertRecordingInfo
        .def_readwrite("f_recording", &skgpu::graphite::InsertRecordingInfo::fRecording)
        .def_readwrite("f_target_surface", &skgpu::graphite::InsertRecordingInfo::fTargetSurface)
        .def_readwrite("f_target_translation", &skgpu::graphite::InsertRecordingInfo::fTargetTranslation)
        .def_readwrite("f_target_clip", &skgpu::graphite::InsertRecordingInfo::fTargetClip)
        .def_readwrite("f_target_texture_state", &skgpu::graphite::InsertRecordingInfo::fTargetTextureState)
        .def_readwrite("f_num_wait_semaphores", &skgpu::graphite::InsertRecordingInfo::fNumWaitSemaphores)
        .def_readwrite("f_wait_semaphores", &skgpu::graphite::InsertRecordingInfo::fWaitSemaphores)
        .def_readwrite("f_num_signal_semaphores", &skgpu::graphite::InsertRecordingInfo::fNumSignalSemaphores)
        .def_readwrite("f_signal_semaphores", &skgpu::graphite::InsertRecordingInfo::fSignalSemaphores)
        .def_readwrite("f_gpu_stats_flags", &skgpu::graphite::InsertRecordingInfo::fGpuStatsFlags)
        .def_readwrite("f_finished_context", &skgpu::graphite::InsertRecordingInfo::fFinishedContext)
        .def_readwrite("f_simulated_status", &skgpu::graphite::InsertRecordingInfo::fSimulatedStatus)
        .def(py::init<>())
    ;

    py::class_<skgpu::graphite::InsertFinishInfo> _InsertFinishInfo(_skia, "InsertFinishInfo");
    registry.on(_skia, "InsertFinishInfo", _InsertFinishInfo);
        _InsertFinishInfo
        .def(py::init<>())
        .def(py::init<skgpu::graphite::GpuFinishedContext, void (*)(void *, skgpu::CallbackResult)>()
        , py::arg("context")
        , py::arg("proc")
        )
        .def(py::init<skgpu::graphite::GpuFinishedContext, void (*)(void *, skgpu::CallbackResult, const skgpu::GpuStats &)>()
        , py::arg("context")
        , py::arg("proc")
        )
        .def_readwrite("f_finished_context", &skgpu::graphite::InsertFinishInfo::fFinishedContext)
        .def_readwrite("f_gpu_stats_flags", &skgpu::graphite::InsertFinishInfo::fGpuStatsFlags)
    ;

    py::enum_<skgpu::graphite::SyncToCpu>(_skia, "SyncToCpu", py::arithmetic())
        .value("K_YES", skgpu::graphite::SyncToCpu::kYes)
        .value("K_NO", skgpu::graphite::SyncToCpu::kNo)
        .export_values()
    ;
    py::enum_<skgpu::graphite::MarkFrameBoundary>(_skia, "MarkFrameBoundary", py::arithmetic())
        .value("K_YES", skgpu::graphite::MarkFrameBoundary::kYes)
        .value("K_NO", skgpu::graphite::MarkFrameBoundary::kNo)
        .export_values()
    ;
    py::class_<skgpu::graphite::SubmitInfo> _SubmitInfo(_skia, "SubmitInfo");
    registry.on(_skia, "SubmitInfo", _SubmitInfo);
        _SubmitInfo
        .def_readwrite("f_sync", &skgpu::graphite::SubmitInfo::fSync)
        .def_readwrite("f_mark_boundary", &skgpu::graphite::SubmitInfo::fMarkBoundary)
        .def_readwrite("f_frame_id", &skgpu::graphite::SubmitInfo::fFrameID)
        .def_readwrite("f_finished_context", &skgpu::graphite::SubmitInfo::fFinishedContext)
        .def(py::init<>())
        .def(py::init<skgpu::graphite::SyncToCpu>()
        , py::arg("sync")
        )
        .def(py::init<skgpu::graphite::SyncToCpu, uint64_t>()
        , py::arg("sync")
        , py::arg("frame_id")
        )
    ;

    py::enum_<skgpu::graphite::Volatile>(_skia, "Volatile", py::arithmetic())
        .value("K_NO", skgpu::graphite::Volatile::kNo)
        .value("K_YES", skgpu::graphite::Volatile::kYes)
        .export_values()
    ;
    py::enum_<skgpu::graphite::DepthStencilFlags>(_skia, "DepthStencilFlags", py::arithmetic())
        .value("K_NONE", skgpu::graphite::DepthStencilFlags::kNone)
        .value("K_DEPTH", skgpu::graphite::DepthStencilFlags::kDepth)
        .value("K_STENCIL", skgpu::graphite::DepthStencilFlags::kStencil)
        .value("K_DEPTH_STENCIL", skgpu::graphite::DepthStencilFlags::kDepthStencil)
        .export_values()
    ;
    py::enum_<skgpu::graphite::SampleCount>(_skia, "SampleCount", py::arithmetic())
        .value("K1", skgpu::graphite::SampleCount::k1)
        .value("K2", skgpu::graphite::SampleCount::k2)
        .value("K4", skgpu::graphite::SampleCount::k4)
        .value("K8", skgpu::graphite::SampleCount::k8)
        .value("K16", skgpu::graphite::SampleCount::k16)
        .export_values()
    ;
    _skia
    .def("to_sample_count", &skgpu::graphite::ToSampleCount
        , py::arg("sample_count")
        )
    ;

    py::enum_<skgpu::graphite::DrawTypeFlags>(_skia, "DrawTypeFlags", py::arithmetic())
        .value("K_NONE", skgpu::graphite::DrawTypeFlags::kNone)
        .value("K_BITMAP_TEXT_MASK", skgpu::graphite::DrawTypeFlags::kBitmapText_Mask)
        .value("K_BITMAP_TEXT_LCD", skgpu::graphite::DrawTypeFlags::kBitmapText_LCD)
        .value("K_BITMAP_TEXT_COLOR", skgpu::graphite::DrawTypeFlags::kBitmapText_Color)
        .value("K_SDF_TEXT", skgpu::graphite::DrawTypeFlags::kSDFText)
        .value("K_SDF_TEXT_LCD", skgpu::graphite::DrawTypeFlags::kSDFText_LCD)
        .value("K_DRAW_VERTICES", skgpu::graphite::DrawTypeFlags::kDrawVertices)
        .value("K_CIRCULAR_ARC", skgpu::graphite::DrawTypeFlags::kCircularArc)
        .value("K_ANALYTIC_R_RECT", skgpu::graphite::DrawTypeFlags::kAnalyticRRect)
        .value("K_PER_EDGE_AA_QUAD", skgpu::graphite::DrawTypeFlags::kPerEdgeAAQuad)
        .value("K_NON_AA_FILL_RECT", skgpu::graphite::DrawTypeFlags::kNonAAFillRect)
        .value("K_SIMPLE_SHAPE", skgpu::graphite::DrawTypeFlags::kSimpleShape)
        .value("K_NON_SIMPLE_SHAPE", skgpu::graphite::DrawTypeFlags::kNonSimpleShape)
        .value("K_DROP_SHADOWS", skgpu::graphite::DrawTypeFlags::kDropShadows)
        .value("K_ANALYTIC_CLIP", skgpu::graphite::DrawTypeFlags::kAnalyticClip)
        .value("K_LAST", skgpu::graphite::DrawTypeFlags::kLast)
        .export_values()
    ;

}