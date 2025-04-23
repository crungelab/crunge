cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Skia.cmake)

set(THIS crunge-skia)
set(MODULE skia)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

pybind11_add_module(${THIS} SHARED src/skia_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_SKIA(${THIS})

set(SOURCES
    src/skia_py_module.cpp
    src/skia_py.cpp
    src/skia_context_py_auto.cpp
    src/skia_surface_py_auto.cpp
    src/skia_canvas_py_auto.cpp
)

target_sources(${THIS} PRIVATE ${SOURCES})

# add include files
target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${SKIA_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})