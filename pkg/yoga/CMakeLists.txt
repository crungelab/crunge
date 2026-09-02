cmake_minimum_required(VERSION 3.30...4.0 FATAL_ERROR)

set(THIS crunge-yoga)
set(MODULE yoga)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Yoga.cmake)

pybind11_add_module(${THIS} MODULE
    src/bindings/yoga_py_module.cpp
    src/bindings/yoga_enums_py_auto.cpp
    src/bindings/yoga_style_py_auto.cpp
    src/bindings/yoga_layout_py.cpp
    src/bindings/yoga_layout_py_auto.cpp

    src/Layout.cpp
    src/Config.cpp

    # Generated but not exposed:
    #src/bindings/yoga_py.cpp
    #src/bindings/yoga_numeric_py_auto.cpp
    #src/bindings/yoga_algorithm_py_auto.cpp
)

cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_YOGA(${THIS})

target_include_directories(${THIS}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${YOGA_ROOT}
)

install(TARGETS ${THIS} LIBRARY DESTINATION crunge/${MODULE})