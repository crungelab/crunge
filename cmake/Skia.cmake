include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_SKIA THIS)
    USES_DAWN(${THIS})

    target_include_directories(${THIS} PRIVATE
        ${SKIA_ROOT}
    )

    target_link_libraries(${THIS} PRIVATE
        ${SKIA_LIB_DIR}/libskia.so
    )
endfunction()
