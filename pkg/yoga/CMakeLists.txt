cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/Yoga.cmake)

set(THIS crunge-yoga)
set(MODULE yoga)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

pybind11_add_module(${THIS} SHARED src/bindings/yoga_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_YOGA(${THIS})

set(SOURCES
    src/Node.cpp
    src/Config.cpp
    src/bindings/yoga_py_module.cpp
    #src/bindings/yoga_py.cpp
    #src/bindings/yoga_numeric_py_auto.cpp
    src/bindings/yoga_enums_py_auto.cpp
    src/bindings/yoga_style_py_auto.cpp
    src/bindings/yoga_node_py.cpp
    src/bindings/yoga_node_py_auto.cpp
    #src/bindings/yoga_algorithm_py_auto.cpp
)

target_sources(${THIS} PRIVATE ${SOURCES})

target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${YOGA_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

set_target_properties(${THIS} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
#set_target_properties(${THIS} PROPERTIES INSTALL_RPATH "$ORIGIN/../core")

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})