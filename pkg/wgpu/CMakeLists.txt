cmake_minimum_required(VERSION 3.4)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Dawn.cmake)

set(THIS crunge-wgpu)
set(MODULE wgpu)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

pybind11_add_module(${THIS} SHARED src/crunge/wgpu/bindings/init.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_DAWN(${THIS})

# install(TARGETS ${THIS} LIBRARY DESTINATION aimgui)

# target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
set(SOURCES
    src/crunge/wgpu/bindings/chained_struct.cpp
    src/crunge/wgpu/bindings/wgpu.cpp
    src/crunge/wgpu/bindings/main.cpp
)

target_sources(${THIS} PRIVATE ${SOURCES})

# add include files
# target_sources(${THIS} PRIVATE ${AIMGUI_INCLUDE}) # for intellisense
target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${DAWN_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})