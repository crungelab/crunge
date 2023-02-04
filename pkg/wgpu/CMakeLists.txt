cmake_minimum_required(VERSION 3.4)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Dawn.cmake)

set(THIS crunge-wgpu)
set(BINARY wgpu)

project(${THIS} VERSION "0.1")

#find_package(PythonExtensions REQUIRED)
# add_library(${THIS} MODULE src/crunge/wgpu/bindings/init.cpp)
#python_extension_module(${THIS})

pybind11_add_module(${THIS} SHARED
    src/crunge/wgpu/bindings/init.cpp
)

configure_project(${THIS} ${BINARY})
USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_DAWN(${THIS})

# install(TARGETS ${THIS} LIBRARY DESTINATION aimgui)

# target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
set(SOURCES
    src/crunge/wgpu/bindings/generated.cpp
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

#
# INSTALL
#
# install headers
# install(FILES ${IMGUI_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")

get_target_property(_RUNTIME_OUTPUT_DIRECTORY ${THIS} RUNTIME_OUTPUT_DIRECTORY)

add_custom_command(
    TARGET ${THIS} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${_RUNTIME_OUTPUT_DIRECTORY}/Debug/_wgpu.pyd
    ${CMAKE_CURRENT_SOURCE_DIR}/crunge/wgpu/_wgpu.pyd
)
