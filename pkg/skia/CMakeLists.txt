cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-skia)
set(MODULE skia)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Skia.cmake)

pybind11_add_module(${THIS} MODULE
    src/skia_py_module.cpp
    src/skia_py.cpp

    src/skia_context_py.cpp
    src/skia_context_py_auto.cpp
    src/skia_surface_py.cpp
    src/skia_surface_py_auto.cpp
    src/skia_canvas_py.cpp
    src/skia_canvas_py_auto.cpp
    src/skia_recorder_py_auto.cpp
    src/skia_recording_py_auto.cpp
    src/standard_recorder_options_py.cpp
    src/skia_graphite_types_py_auto.cpp

    src/skia_paint_py.cpp
    src/skia_paint_py_auto.cpp
    src/skia_shader_py.cpp
    src/skia_color_py.cpp
    src/skia_color_py_auto.cpp
    src/skia_color_space_py_auto.cpp
    src/skia_color_type_py_auto.cpp
    src/skia_alpha_type_py_auto.cpp
    src/skia_blend_mode_py_auto.cpp
    src/skia_tile_mode_py_auto.cpp
    src/skia_clip_op_py_auto.cpp

    src/skia_rect_py.cpp
    src/skia_rect_py_auto.cpp
    src/skia_size_py_auto.cpp
    src/skia_point_py.cpp
    src/skia_point_py_auto.cpp
    src/skia_matrix_py_auto.cpp
    src/skia_path_py_auto.cpp
    src/skia_path_builder_py_auto.cpp

    src/skia_font_types_py_auto.cpp
    src/skia_font_py.cpp
    src/skia_font_py_auto.cpp
    src/skia_text_blob_py_auto.cpp

    src/skia_image_py_auto.cpp
    src/skia_image_info_py_auto.cpp
    src/skia_image_filter_py_auto.cpp
    src/skia_sampling_options_py_auto.cpp
    src/skia_data_py_auto.cpp

    src/effects/skia_gradient_py.cpp
    src/effects/skia_gradient_py_auto.cpp
    src/effects/skia_perlin_noise_shader_py.cpp
    src/effects/skia_image_filters_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_SKIA(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${SKIA_ROOT}
)

set_target_properties(${THIS} PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN/../native"
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})