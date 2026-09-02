cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-sdl)
set(MODULE sdl)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Sdl.cmake)
include(../../cmake/SdlMixer.cmake)

find_package(Python 3.12 REQUIRED COMPONENTS Interpreter Development.Module)

pybind11_add_module(${THIS} MODULE
    src/sdl_py_module.cpp
    src/sdl_py.cpp
    src/sdl_init_py_auto.cpp
    src/sdl_video_py_auto.cpp
    src/sdl_events_py_auto.cpp
    src/sdl_keyboard_py_auto.cpp
    src/sdl_mouse_py_auto.cpp
    src/sdl_scancode_py_auto.cpp
    src/sdl_properties_py_auto.cpp
    src/sdl_audio_py.cpp
    src/sdl_audio_py_auto.cpp
    src/mixer/sdl_mixer_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_SDL(${THIS})
USES_SDL_MIXER(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${SDL_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})