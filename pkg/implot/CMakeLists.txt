cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-implot)
set(MODULE implot)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/ImGui.cmake)

pybind11_add_module(${THIS} MODULE
    src/implot_py_module.cpp
    src/implot_py.cpp
    src/implot_py_auto.cpp

    ${IMPLOT_ROOT}/implot.cpp
    ${IMPLOT_ROOT}/implot_items.cpp
    ${IMPLOT_ROOT}/implot_demo.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_IMGUI(${THIS})

target_compile_definitions(${THIS} PRIVATE IMPLOT_DISABLE_OBSOLETE_FUNCTIONS)

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${IMPLOT_ROOT}
)

set_target_properties(${THIS} PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN/../imgui"
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})