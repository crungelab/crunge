include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Config.cmake)

function(USES_STD THIS)
    target_include_directories(${THIS} PRIVATE ${DEPOT_ROOT})

    target_compile_definitions(${THIS} PRIVATE ${CRUNGE_COMPILE_DEFS})

    target_compile_features(${THIS} PUBLIC cxx_std_20)

    if(MSVC)
        target_compile_options(${THIS} PRIVATE /bigobj)
        if(MSVC_VERSION GREATER_EQUAL 1914)
            target_compile_options(${THIS} PRIVATE /Zc:__cplusplus)
        endif()
    endif()
endfunction()

# Name the built module so Python can import it as crunge.<module>._<module>
function(configure_project project binary)
  set_target_properties(${project} PROPERTIES
    OUTPUT_NAME ${binary}
    PREFIX "_"
  )
endfunction()