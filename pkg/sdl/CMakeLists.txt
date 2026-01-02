cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Sdl.cmake)

set(THIS crunge-sdl)
set(MODULE sdl)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

set(HEADERS
)

set(SOURCES
    src/sdl_init_py_auto.cpp
    src/sdl_video_py_auto.cpp
    #src/sdl_audio_py_auto.cpp #TODO: Fix audio bindings
    src/sdl_events_py_auto.cpp
    src/sdl_keyboard_py_auto.cpp
    src/sdl_mouse_py_auto.cpp
    src/sdl_scancode_py_auto.cpp
    src/sdl_properties_py_auto.cpp
    src/sdl_py.cpp
)

pybind11_add_module(${THIS} MODULE src/sdl_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_SDL(${THIS})

target_sources(${THIS} PRIVATE ${SOURCES} ${HEADERS})

target_include_directories(${THIS}
	PUBLIC
		$<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${SDL_ROOT}>
	PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})