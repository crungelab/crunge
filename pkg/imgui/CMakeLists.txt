cmake_minimum_required(VERSION 3.4)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)

set(THIS crunge-imgui)
set(BINARY imgui)

project(${THIS} VERSION "0.1")

find_package(PythonExtensions REQUIRED)

set(IMGUI_HEADERS
    ${IMGUI_ROOT}/imconfig.h
    ${IMGUI_ROOT}/imgui_internal.h
    ${IMGUI_ROOT}/imgui.h
    ${IMGUI_ROOT}/imstb_rectpack.h
    ${IMGUI_ROOT}/imstb_textedit.h
    ${IMGUI_ROOT}/imstb_truetype.h
)

set(IMGUI_SRC
    src/crunge/imgui/bindings/generated.cpp
    src/crunge/imgui/bindings/main.cpp
    ${IMGUI_ROOT}/imgui_demo.cpp
    ${IMGUI_ROOT}/imgui_draw.cpp
    ${IMGUI_ROOT}/imgui_tables.cpp
    ${IMGUI_ROOT}/imgui_widgets.cpp
    ${IMGUI_ROOT}/imgui.cpp
)

add_library(${THIS} SHARED src/crunge/imgui/bindings/init.cpp)
python_extension_module(${THIS})
configure_project(${THIS} ${BINARY})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})

#install(TARGETS ${THIS} LIBRARY DESTINATION aimgui)

target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
target_compile_definitions(${THIS} PRIVATE NULL=nullptr)

target_sources(${THIS} PRIVATE ${IMGUI_SRC} ${IMGUI_HEADERS})

# add include files
#target_sources(${THIS} PRIVATE ${AIMGUI_INCLUDE}) # for intellisense

target_include_directories(${THIS}
	PUBLIC
		$<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${IMGUI_ROOT}>
	PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)
#
# INSTALL
#
# install headers
install(FILES ${IMGUI_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})


# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")

get_target_property(_RUNTIME_OUTPUT_DIRECTORY ${THIS} RUNTIME_OUTPUT_DIRECTORY)

add_custom_command(
        TARGET ${THIS} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
                ${_RUNTIME_OUTPUT_DIRECTORY}/Debug/_imgui.pyd
                ${CMAKE_CURRENT_SOURCE_DIR}/crunge/imgui/_imgui.pyd
                )
