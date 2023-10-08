cmake_minimum_required(VERSION 3.4)

set(THIS hello-wgpu)
project(${THIS} LANGUAGES CXX)

include(../../cmake/Dawn.cmake)

set(HEADERS
)

set(SOURCES
    main.cpp
)

add_executable(${THIS} ${HEADERS} ${SOURCES})
USES_DAWN(${THIS})
