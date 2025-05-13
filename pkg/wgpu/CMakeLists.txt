cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Dawn.cmake)

set(THIS crunge-wgpu)
set(MODULE wgpu)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

pybind11_add_module(${THIS} SHARED src/wgpu_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_DAWN(${THIS})

set(SOURCES
    src/chained_struct.cpp
    src/pywgpu.cpp
    src/wgpu_py.cpp
    src/wgpu_py_auto.cpp
    src/callbacks.cpp
    src/callbacks_py.cpp
)

target_sources(${THIS} PRIVATE ${SOURCES})

# add include files
target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${DAWN_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

set_target_properties(${THIS} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/../core")

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})