include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_SDL_MIXER THIS)
    USES_STD(${THIS})
    target_include_directories(${THIS} PRIVATE
        ${SDL_MIXER_ROOT}/include
    )
    target_link_libraries(${THIS} PRIVATE SDL3_mixer-static)
endfunction()

