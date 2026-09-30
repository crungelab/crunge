cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-rtaudio)
set(MODULE rtaudio)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/RtAudio.cmake)

pybind11_add_module(${THIS} MODULE
    src/rtaudio_py_module.cpp
    src/audio_stream.cpp
    src/audio_stream_py_auto.cpp

    src/rtaudio_py.cpp
    src/rtaudio_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_RTAUDIO(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${RTAUDIO_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})