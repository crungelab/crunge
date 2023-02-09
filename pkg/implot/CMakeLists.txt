cmake_minimum_required(VERSION 3.4)

set(THIS crunge-implot)
set(BINARY implot)

project(${THIS} VERSION "0.1")

include(../../cmake/ImGui.cmake)

set(IMPLOT_HEADERS
    ${IMPLOT_ROOT}/implot.h
    ${IMPLOT_ROOT}/implot_internal.h
)

set(IMPLOT_SRC
    src/crunge/implot/bindings/generated.cpp
    src/crunge/implot/bindings/main.cpp
    ${IMPLOT_ROOT}/implot_demo.cpp
    ${IMPLOT_ROOT}/implot_items.cpp
    ${IMPLOT_ROOT}/implot.cpp
)

pybind11_add_module(${THIS} MODULE
    src/crunge/implot/bindings/init.cpp
)
configure_project(${THIS} ${BINARY})

USES_IMGUI(${THIS})

target_compile_definitions(${THIS} PRIVATE IMPLOT_DISABLE_OBSOLETE_FUNCTIONS)

# install(TARGETS ${THIS} EXPORT crunge/implotTargets
# LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
# ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
# )
target_sources(${THIS} PRIVATE ${IMPLOT_SRC} ${IMPLOT_HEADERS})

# add include files
# target_sources(${THIS} PRIVATE ${crunge/implot_INCLUDE}) # for intellisense
target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${AIMGUI_ROOT}/include>
    $<BUILD_INTERFACE:${IMGUI_ROOT}>
    $<BUILD_INTERFACE:${IMPLOT_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

#
# INSTALL
#
# install headers
# install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES ${IMPLOT_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# install(TARGETS crunge/implot DESTINATION .)
# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")

get_target_property(_RUNTIME_OUTPUT_DIRECTORY ${THIS} RUNTIME_OUTPUT_DIRECTORY)

add_custom_command(
    TARGET ${THIS} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${_RUNTIME_OUTPUT_DIRECTORY}/Debug/_implot.pyd
    ${CMAKE_CURRENT_SOURCE_DIR}/crunge/implot/_implot.pyd
)
