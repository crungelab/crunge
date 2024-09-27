cmake_minimum_required(VERSION 3.5)

include(../../cmake/ImGui.cmake)

set(THIS crunge-implot)
set(MODULE implot)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

set(IMPLOT_HEADERS
    ${IMPLOT_ROOT}/implot.h
    ${IMPLOT_ROOT}/implot_internal.h
)

set(IMPLOT_SRC
    src/implot_py_auto.cpp
    src/implot_py.cpp
    ${IMPLOT_ROOT}/implot_demo.cpp
    ${IMPLOT_ROOT}/implot_items.cpp
    ${IMPLOT_ROOT}/implot.cpp
)

pybind11_add_module(${THIS} MODULE
    src/implot_py_module.cpp
)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_IMGUI(${THIS})

target_compile_definitions(${THIS} PRIVATE IMPLOT_DISABLE_OBSOLETE_FUNCTIONS)

target_sources(${THIS} PRIVATE ${IMPLOT_SRC} ${IMPLOT_HEADERS})

target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${IMGUI_ROOT}>
    $<BUILD_INTERFACE:${IMPLOT_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

set_target_properties(${THIS} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
#set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/")
set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/../imgui")

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})