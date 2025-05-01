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
    py::class_<skgpu::graphite::InsertRecordingInfo> InsertRecordingInfo(_skia, "InsertRecordingInfo");
    registry.on(_skia, "InsertRecordingInfo", InsertRecordingInfo);
        InsertRecordingInfo
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
        .def(py::init<>())
    ;

    py::class_<skgpu::graphite::InsertFinishInfo> InsertFinishInfo(_skia, "InsertFinishInfo");
    registry.on(_skia, "InsertFinishInfo", InsertFinishInfo);
        InsertFinishInfo
        .def(py::init<>())
        .def_readwrite("f_finished_context", &skgpu::graphite::InsertFinishInfo::fFinishedContext)
        .def_readwrite("f_gpu_stats_flags", &skgpu::graphite::InsertFinishInfo::fGpuStatsFlags)
    ;

    py::enum_<skgpu::graphite::SyncToCpu>(_skia, "SyncToCpu", py::arithmetic())
        .value("K_YES", skgpu::graphite::SyncToCpu::kYes)
        .value("K_NO", skgpu::graphite::SyncToCpu::kNo)
        .export_values()
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

    py::enum_<skgpu::graphite::DrawTypeFlags>(_skia, "DrawTypeFlags", py::arithmetic())
        .value("K_NONE", skgpu::graphite::DrawTypeFlags::kNone)
        .value("K_BITMAP_TEXT_MASK", skgpu::graphite::DrawTypeFlags::kBitmapText_Mask)
        .value("K_BITMAP_TEXT_LCD", skgpu::graphite::DrawTypeFlags::kBitmapText_LCD)
        .value("K_BITMAP_TEXT_COLOR", skgpu::graphite::DrawTypeFlags::kBitmapText_Color)
        .value("K_SDF_TEXT", skgpu::graphite::DrawTypeFlags::kSDFText)
        .value("K_SDF_TEXT_LCD", skgpu::graphite::DrawTypeFlags::kSDFText_LCD)
        .value("K_DRAW_VERTICES", skgpu::graphite::DrawTypeFlags::kDrawVertices)
        .value("K_CIRCULAR_ARC", skgpu::graphite::DrawTypeFlags::kCircularArc)
        .value("K_SIMPLE_SHAPE", skgpu::graphite::DrawTypeFlags::kSimpleShape)
        .value("K_NON_SIMPLE_SHAPE", skgpu::graphite::DrawTypeFlags::kNonSimpleShape)
        .value("K_LAST", skgpu::graphite::DrawTypeFlags::kLast)
        .export_values()
    ;


}