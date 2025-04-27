include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_DAWN THIS)
    USES_STD(${THIS})

    target_include_directories(${THIS} PRIVATE
        ${DAWN_ROOT}/include
        ${SKIA_LIB_DIR}/gen/third_party/externals/dawn/include
        ${CRUNGE_ROOT}/pkg/wgpu/include # Override dawn/webgpu_cpp.h
    )

    target_link_libraries(${THIS} PRIVATE
        ${SKIA_LIB_DIR}/libdawn_native.so
        ${SKIA_LIB_DIR}/libdawn_proc.so
        ${SKIA_LIB_DIR}/libwebgpu_dawn.so
    )    

    #target_include_directories(${THIS} PRIVATE
    #    ${DAWN_ROOT}/include
    #)

    #target_link_libraries(${THIS} PRIVATE
    #    dawn_internal_config
    #    dawncpp
    #    dawn_proc
    #    dawn_common
        #dawn_glfw
    #    dawn_native
    #    dawn_wire
        #dawn_utils
        #glfw
    #)
endfunction()
