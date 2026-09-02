cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-gltf)
set(MODULE gltf)

project(${THIS} VERSION "0.1" LANGUAGES C CXX)

include(../../cmake/Gltf.cmake)

pybind11_add_module(${THIS} MODULE
    src/gltf_py_module.cpp
    src/gltf_py.cpp
    src/gltf_py_auto.cpp

    src/mikktspace/mikktspace.c
    src/mikktspace_py.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_GLTF(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${GLTF_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})