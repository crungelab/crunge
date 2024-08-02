include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_DAWN THIS)
    USES_STD(${THIS})

    target_include_directories(${THIS} PRIVATE
        ${DAWN_ROOT}/include
    )

    target_link_libraries(${THIS} PRIVATE
        dawn_internal_config
        dawncpp
        dawn_proc
        dawn_common
        #dawn_glfw
        dawn_native
        dawn_wire
        #dawn_utils
        #glfw
    )
endfunction()
