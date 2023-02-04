include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_DAWN THIS)
    USES_STD(${THIS})

    # target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
    target_include_directories(${THIS} PRIVATE
        ${DAWN_ROOT}/inc
    )
    target_link_directories(${THIS} PRIVATE
        ${DAWN_ROOT}/bin/win/x64
    )
    target_link_libraries(${THIS} PRIVATE
        dawn_native.dll.lib
        dawn_proc.dll.lib
    )
endfunction()
