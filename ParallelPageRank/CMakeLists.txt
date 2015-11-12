# Most of this is derived from an existing CMake file I had --AG
cmake_minimum_required (VERSION 3.0.2)
project (Ranker)

# Derived from http://stackoverflow.com/a/30564223
if (CMAKE_VERSION VERSION_LESS "3.1")
  if (CMAKE_C_COMPILER_ID STREQUAL "GNU")
    set (CMAKE_C_FLAGS "--std=gnu99 -fopenmp ${CMAKE_C_FLAGS}")
  endif ()
else ()
  set (CMAKE_C_STANDARD 99)
endif ()
# End stackoverflow derived

# This supports testing using the Check C unit testing package. It
# adds autogeneration of C source from the format which checkmk
# accepts. See the tests directory for the setup for the tests in
# CMake.
macro (build_test test)
  add_custom_command (
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${test}.c
    MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/${test}.ts
    COMMAND checkmk ${CMAKE_CURRENT_SOURCE_DIR}/${test}.ts > ${CMAKE_CURRENT_BINARY_DIR}/${test}.c
    )
endmacro (build_test)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

enable_testing()
add_subdirectory(src)
add_subdirectory(tests)