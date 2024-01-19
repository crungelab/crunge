include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_SDL THIS)
    USES_STD(${THIS})
    target_include_directories(${THIS} PRIVATE
        ${SDL_ROOT}/src
    )
    target_link_libraries(${THIS} PRIVATE SDL3-static)
endfunction()

