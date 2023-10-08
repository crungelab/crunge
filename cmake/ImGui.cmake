include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Core.cmake)

function(USES_IMGUI THIS)
    USES_CORE(${THIS})
    target_compile_definitions(${THIS} PRIVATE IMGUI_USER_CONFIG=<crunge/imgui/imconfig.h>)
    target_compile_definitions(${THIS} PRIVATE NULL=nullptr)
    target_include_directories(${THIS} PRIVATE
        ${IMGUI_ROOT}
    )
    target_link_libraries(${THIS} PRIVATE crunge-imgui)
endfunction()
