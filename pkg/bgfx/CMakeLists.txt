cmake_minimum_required(VERSION 3.4)

set(THIS crunge-bgfx)
set(BINARY bgfx)

project(${THIS} VERSION "0.1")

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)

set(INCLUDES
    include/crunge/bgfx/crunge-bgfx.h
)

set(SOURCES
    src/crunge/bgfx/bindings/bgfx.cpp
    src/crunge/bgfx/bindings/platform.cpp
    src/crunge/bgfx/bindings/embedded_shader.cpp
    src/crunge/bgfx/bindings/main.cpp
)

pybind11_add_module(${THIS} SHARED
    src/crunge/bgfx/bindings/init.cpp
)
configure_project(${THIS} ${BINARY})
USES_PYBIND11(${THIS})
USES_CORE(${THIS})

#install(TARGETS ${THIS} EXPORT AimGfxTargets
#	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
#	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
#)

target_sources(${THIS} PRIVATE
    ${SOURCES} ${INCLUDES}
)

# add include files
target_sources(${THIS} PRIVATE ${SOURCES} ${INCLUDES}) # for intellisense
target_include_directories(${THIS}
	PUBLIC
		$<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${BGFX_ROOT}>
	PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${BX_ROOT}/include/compat/msvc
        ${BX_ROOT}/include
        ${BX_ROOT}/3rdparty
        ${BIMG_ROOT}/include
        ${BIMG_ROOT}/3rdparty
        ${BGFX_ROOT}/include
        ${BGFX_ROOT}/3rdparty
        ${BGFX_ROOT}/3rdparty/khronos
        ${BGFX_ROOT}/3rdparty/dxsdk/include
)

target_link_libraries(${THIS} PRIVATE
    bimg
    bgfx
)

#
# INSTALL
#
# install headers
#install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES ${BGFX_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})


#install(TARGETS aimgfx DESTINATION .)
# Quiet a warning, since this project is only valid with SKBUILD
set(ignoreMe "${SKBUILD}")

get_target_property(_RUNTIME_OUTPUT_DIRECTORY ${THIS} RUNTIME_OUTPUT_DIRECTORY)

add_custom_command(
        TARGET ${THIS} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
                ${_RUNTIME_OUTPUT_DIRECTORY}/Debug/_bgfx.pyd
                ${CMAKE_CURRENT_SOURCE_DIR}/crunge/bgfx/_bgfx.pyd
                )
