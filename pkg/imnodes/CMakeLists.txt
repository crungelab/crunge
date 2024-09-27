cmake_minimum_required(VERSION 3.5)

include(../../cmake/ImGui.cmake)

set(THIS crunge-imnodes)
set(MODULE imnodes)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

set(IMNODES_HEADERS
    ${IMNODES_ROOT}/imnodes.h
    ${IMNODES_ROOT}/imnodes_internal.h
    include/crunge/imnodes/imnodes_config.h
)

set(IMNODES_SRC
    ${IMNODES_ROOT}/imnodes.cpp
    src/imnodes_py_auto.cpp
    src/imnodes_py.cpp
)

pybind11_add_module(${THIS} MODULE
    src/imnodes_py_module.cpp
)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_IMGUI(${THIS})

target_compile_definitions(${THIS} PRIVATE IMNODES_USER_CONFIG=<crunge/imnodes/imnodes_config.h>)

target_sources(${THIS} PRIVATE ${IMNODES_SRC} ${IMNODES_HEADERS})

target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${IMGUI_ROOT}>
    $<BUILD_INTERFACE:${IMNODES_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

set_target_properties(${THIS} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
#set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/")
set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/../imgui")

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})