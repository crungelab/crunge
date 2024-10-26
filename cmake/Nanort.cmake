include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_NANORT THIS)
    USES_STD(${THIS})
    target_include_directories(${THIS} PRIVATE
        ${NANORT_ROOT}/src
    )
    #target_link_libraries(${THIS} PRIVATE nanort)
endfunction()
