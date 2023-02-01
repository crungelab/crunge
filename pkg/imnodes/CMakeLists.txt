cmake_minimum_required(VERSION 3.4)

set(THIS crunge-imnodes)
set(BINARY imnodes)

project(${THIS} VERSION "0.1")

include(../../cmake/ImGui.cmake)

set(IMNODES_ROOT ${CRUNGE_ROOT}/depot/imnodes)

set(IMNODES_HEADERS
    ${IMNODES_ROOT}/imnodes.h
    ${IMNODES_ROOT}/imnodes_internal.h
    src/crunge/imnodes/imnodes_config.h
)

set(IMNODES_SRC
    ${IMNODES_ROOT}/imnodes.cpp
    src/crunge/imnodes/bindings/generated.cpp
    src/crunge/imnodes/bindings/main.cpp
)

pybind11_add_module(${THIS} MODULE
    src/crunge/imnodes/bindings/init.cpp
)
USES_IMGUI(${THIS})
configure_project(${THIS} ${BINARY})

target_compile_definitions(${THIS} PRIVATE IMNODES_USER_CONFIG=<crunge/imnodes/imnodes_config.h>)

# install(TARGETS imnodes EXPORT AimNodesTargets
# LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
# ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
# )
target_sources(${THIS} PRIVATE ${IMNODES_SRC} ${IMNODES_HEADERS})

# add include files
# target_sources(${THIS} PRIVATE ${AIMNODES_INCLUDE}) # for intellisense
target_include_directories(${THIS}
    PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${AIMGUI_ROOT}/include>
    $<BUILD_INTERFACE:${IMGUI_ROOT}>
    $<BUILD_INTERFACE:${IMNODES_ROOT}>
    PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

#
# INSTALL
#
# install headers
# install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES ${IMNODES_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# install(TARGETS imnodes DESTINATION .)
# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")

get_target_property(_RUNTIME_OUTPUT_DIRECTORY ${THIS} RUNTIME_OUTPUT_DIRECTORY)

add_custom_command(
    TARGET ${THIS} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${_RUNTIME_OUTPUT_DIRECTORY}/Debug/_imnodes.pyd
    ${CMAKE_CURRENT_SOURCE_DIR}/crunge/imnodes/_imnodes.pyd
)
