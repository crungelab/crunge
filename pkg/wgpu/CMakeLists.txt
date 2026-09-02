cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-wgpu)
set(MODULE wgpu)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Dawn.cmake)

pybind11_add_module(${THIS} MODULE
    src/wgpu_py_module.cpp
    src/wgpu_py.cpp
    src/wgpu_py_auto.cpp
    src/pywgpu.cpp
    src/chained_struct.cpp
    src/callbacks.cpp
    src/callbacks_py.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_DAWN(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${DAWN_ROOT}
)

set_target_properties(${THIS} PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN/../native"
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})