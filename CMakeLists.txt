cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

# SDL, Box2D, and RtAudio are C. Declaring both here checks the C compiler
# once up front instead of letting each subproject enable it ad hoc.
project(CRUNGE VERSION 0.1.0 LANGUAGES C CXX)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
include(Config)

#
# Global toolchain settings. These are inherited by every add_subdirectory()
# below, so anything set here must be wanted by all of them.
#
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(BUILD_SHARED_LIBS OFF)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Generic names honoured by most of the depot projects.
set(BUILD_TESTING OFF)
set(BUILD_EXAMPLES OFF)
set(BUILD_SHARED OFF)
set(BUILD_STATIC ON)

#
# Python / pybind11 / cxbind
#
set(PYBIND11_FINDPYTHON ON)
find_package(Python 3.12 REQUIRED COMPONENTS Interpreter Development.Module Development.Embed)

add_subdirectory(depot/pybind11 EXCLUDE_FROM_ALL)
find_package(cxbind REQUIRED)

#
# Third-party dependencies
#
set(SDL_SHARED OFF)
set(SDL_STATIC ON)
set(SDL_TEST OFF)
set(SDL_RENDER OFF)
set(SDL_INSTALL OFF)
add_subdirectory(depot/sdl EXCLUDE_FROM_ALL)

set(SDLMIXER_INSTALL OFF)
add_subdirectory(depot/sdl_mixer EXCLUDE_FROM_ALL)

set(TINYGLTF_INSTALL OFF)
set(TINYGLTF_BUILD_LOADER_EXAMPLE OFF)
add_subdirectory(depot/tinygltf EXCLUDE_FROM_ALL)

add_subdirectory(depot/yoga EXCLUDE_FROM_ALL)

set(TMXLITE_STATIC_LIB TRUE)
add_subdirectory(depot/tmxlite/tmxlite EXCLUDE_FROM_ALL)

add_subdirectory(depot/box2d EXCLUDE_FROM_ALL)

set(RTAUDIO_BUILD_TESTING OFF)
add_subdirectory(${RTAUDIO_ROOT} ${CMAKE_BINARY_DIR}/depot/rtaudio EXCLUDE_FROM_ALL)

#
# Bindings
#
add_subdirectory(pkg/sdl)
add_subdirectory(pkg/imgui)
add_subdirectory(pkg/implot)
add_subdirectory(pkg/imnodes)
add_subdirectory(pkg/gltf)
add_subdirectory(pkg/wgpu)
add_subdirectory(pkg/skia)
add_subdirectory(pkg/yoga)
add_subdirectory(pkg/nanort)
add_subdirectory(pkg/tmx)
add_subdirectory(pkg/box2d)
add_subdirectory(pkg/augr)