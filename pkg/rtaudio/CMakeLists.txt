cmake_minimum_required(VERSION 3.5)

include(../../cmake/Pybind11.cmake)
include(../../cmake/Core.cmake)
include(../../cmake/RtAudio.cmake)

set(THIS crunge-rtaudio)
set(MODULE rtaudio)

project(${THIS} VERSION "0.1" LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development)

set(HEADERS
)

set(SOURCES
    src/rtaudio_py.cpp
    src/rtaudio_py_auto.cpp
    src/augr.cpp
    src/augr_py_auto.cpp
)

pybind11_add_module(${THIS} MODULE src/rtaudio_py_module.cpp)
cxbind_module(${THIS})
configure_project(${THIS} ${MODULE})

USES_PYBIND11(${THIS})
USES_CORE(${THIS})
USES_RTAUDIO(${THIS})

target_sources(${THIS} PRIVATE ${SOURCES} ${HEADERS})

target_include_directories(${THIS}
	PUBLIC
		$<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<BUILD_INTERFACE:${RTAUDIO_ROOT}>
	PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

install(TARGETS ${THIS} DESTINATION crunge/${MODULE})