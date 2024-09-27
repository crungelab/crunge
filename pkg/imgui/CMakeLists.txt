cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)

set(THIS crunge-imgui)
set(MODULE imgui)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

set(IMGUI_HEADERS
    ${IMGUI_ROOT}/imconfig.h
    ${IMGUI_ROOT}/imgui_internal.h
    ${IMGUI_ROOT}/imgui.h
    ${IMGUI_ROOT}/imstb_rectpack.h
    ${IMGUI_ROOT}/imstb_textedit.h
    ${IMGUI_ROOT}/imstb_truetype.h
)

set(IMGUI_SRC
    src/imgui_py_auto.cpp
    src/imgui_py.cpp
    ${IMGUI_ROOT}/imgui_demo.cpp
    ${IMGUI_ROOT}/imgui_draw.cpp
    ${IMGUI_ROOT}/imgui_tables.cpp
    ${IMGUI_ROOT}/imgui_widgets.cpp
    ${IMGUI_ROOT}/imgui.cpp
)

#pybind11_add_module(${THIS} MODULE src/init.cpp)
pybind11_add_module(${THIS} SHARED src/imgui_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})

target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
target_compile_definitions(${THIS} PRIVATE NULL=nullptr)

target_sources(${THIS} PRIVATE ${IMGUI_SRC} ${IMGUI_HEADERS})

target_include_directories(${THIS}
	PUBLIC
		$<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${IMGUI_ROOT}>
	PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})