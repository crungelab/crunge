cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-imgui)
set(MODULE imgui)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)

pybind11_add_module(${THIS} SHARED
    src/imgui_py_module.cpp
    src/imgui_py.cpp
    src/imgui_py_auto.cpp
    src/imgui_internal_py.cpp

    ${IMGUI_ROOT}/imgui.cpp
    ${IMGUI_ROOT}/imgui_demo.cpp
    ${IMGUI_ROOT}/imgui_draw.cpp
    ${IMGUI_ROOT}/imgui_tables.cpp
    ${IMGUI_ROOT}/imgui_widgets.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})

target_compile_definitions(${THIS}
    PRIVATE
        IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>
)

target_include_directories(${THIS}
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${IMGUI_ROOT}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})