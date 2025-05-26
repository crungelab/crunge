include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_YOGA THIS)
    USES_STD(${THIS})
    target_link_libraries(${THIS} PRIVATE yogacore)
endfunction()

