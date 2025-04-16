cmake_minimum_required(VERSION 3.4...3.20 FATAL_ERROR)

#set(CMAKE_C_COMPILER "/usr/bin/clang")
#set(CMAKE_CXX_COMPILER "/usr/bin/clang++")

project(CRUNGE VERSION 0.1.0 LANGUAGES CXX)

include(./cmake/Config.cmake)

if (POLICY CMP0054)
    cmake_policy(SET CMP0054 NEW)
endif()

if (POLICY CMP0069)
    cmake_policy(SET CMP0069 NEW)
endif()

if (POLICY CMP0077)
    cmake_policy(SET CMP0077 NEW)
endif()

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set (CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})


#
# pybind11
#
#set(-DCMAKE_CXX_STANDARD=20 -std=c++20)
#set(PYBIND11_PYTHON_VERSION 3.10)

add_subdirectory(depot/pybind11)
find_package(cxbind REQUIRED)

#
# ImGui and friends
#
add_subdirectory(pkg/imgui)
add_subdirectory(pkg/implot)
add_subdirectory(pkg/imnodes)

#
# TinyGLTF
#
add_subdirectory(depot/gltf)
set_target_properties(tinygltf PROPERTIES POSITION_INDEPENDENT_CODE ON)

add_subdirectory(pkg/gltf)

#
# Dawn
#

#set(DAWN_BUILD_SAMPLES OFF CACHE BOOL "Build Samples" FORCE)
#set(DAWN_FETCH_DEPENDENCIES ON)
#add_subdirectory("depot/dawn" EXCLUDE_FROM_ALL)

add_subdirectory(pkg/wgpu)

#
# SDL
#
set(HAVE_LIBC ON)
set(SDL_SHARED OFF CACHE BOOL "Build a shared version of the library" FORCE)
set(SDL_STATIC ON CACHE BOOL "Build a static version of the library" FORCE)
set(SDL_TEST OFF CACHE BOOL "Build the SDL3_test library" FORCE)

set(SDL_RENDER OFF CACHE BOOL "Use render subsystem" FORCE)
#set(SDL_AUDIO OFF CACHE BOOL "Use audio subsystem" FORCE)
#set(SDL_HAPTIC OFF CACHE BOOL "Use haptic subsystem" FORCE)

#set(SDL_X11 ${WG_WM_X11} CACHE BOOL "Enable X11 support" FORCE)
#set(SDL_WAYLAND ${WG_WM_WAYLAND} CACHE BOOL "Enable Wayland support" FORCE)

add_subdirectory(depot/sdl)
set_target_properties(SDL3-static PROPERTIES POSITION_INDEPENDENT_CODE ON)

add_subdirectory(pkg/sdl)

#
# Nanort
#
add_subdirectory(pkg/nanort)

