include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/Standard.cmake)

function(USES_PYBIND11 THIS)
  USES_STD(${THIS})
  target_include_directories(${THIS} PRIVATE
    ${PYBIND11_ROOT}/include()
  )
endfunction()

function(configure_project project binary)
  set_target_properties(${project} PROPERTIES OUTPUT_NAME ${binary})
  set_target_properties(${project} PROPERTIES PREFIX "_")

  # if(CMAKE_COMPILER_IS_GNUCXX)
  # set_target_properties(${project} PROPERTIES SUFFIX ".so")
  # else()
  # set_target_properties(${project} PROPERTIES SUFFIX ".pyd")
  # endif(CMAKE_COMPILER_IS_GNUCXX)
  if(ATT_PLATFORM_WINDOWS)
    set_target_properties(${THIS} PROPERTIES SUFFIX ".pyd")
  endif(ATT_PLATFORM_WINDOWS)
endfunction()