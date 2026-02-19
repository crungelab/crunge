include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_BOX2D THIS)
    USES_STD(${THIS})
    target_include_directories(${THIS} PRIVATE
        ${BOX2D_ROOT}/box2d/include
    )
    target_link_libraries(${THIS} PRIVATE box2d)
endfunction()

