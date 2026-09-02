cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-augr)
set(MODULE augr)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/RtAudio.cmake)

pybind11_add_module(${THIS} MODULE
    src/augr_py_module.cpp
    src/augr.cpp
    src/augr_py_auto.cpp

    src/rtaudio_py.cpp
    src/rtaudio_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_RTAUDIO(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${RTAUDIO_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})