include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_TMX THIS)
    USES_STD(${THIS})
    target_include_directories(${THIS} PRIVATE
        ${TMX_ROOT}/tmxlite/include
    )
    target_link_libraries(${THIS} PRIVATE tmxlite)
endfunction()

