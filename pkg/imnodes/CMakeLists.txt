cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-imnodes)
set(MODULE imnodes)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/ImGui.cmake)

pybind11_add_module(${THIS} MODULE
    src/imnodes_py_module.cpp
    src/imnodes_py.cpp
    src/imnodes_py_auto.cpp

    ${IMNODES_ROOT}/imnodes.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_IMGUI(${THIS})

target_compile_definitions(${THIS}
    PRIVATE
        IMNODES_USER_CONFIG=<crunge/imnodes/imnodes_config.h>
)

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${IMNODES_ROOT}
)

set_target_properties(${THIS} PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "$ORIGIN/../imgui"
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})