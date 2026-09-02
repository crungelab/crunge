cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-nanort)
set(MODULE nanort)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Nanort.cmake)

pybind11_add_module(${THIS} MODULE
    src/nanort_py_module.cpp
    src/nanort_py.cpp
    src/nanort_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_NANORT(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${NANORT_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})