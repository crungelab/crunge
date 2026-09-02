cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-box2d)
set(MODULE box2d)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Box2D.cmake)

pybind11_add_module(${THIS} MODULE
    src/box2d_py_module.cpp
    src/box2d_py_auto.cpp

    src/types_py.cpp
    src/types_py_auto.cpp
    src/id_py.cpp
    src/id_py_auto.cpp

    src/math_functions_py.cpp
    src/math_functions_py_auto.cpp
    src/collision_py_auto.cpp

    src/debug_draw_py.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_BOX2D(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${BOX2D_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})