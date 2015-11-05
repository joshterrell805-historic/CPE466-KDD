# This is derived from a CMake file I had sitting around --AG
macro (do_test test lib)
  # This macro is defined in the top-level CMakeLists.txt
  build_test(${test})
  add_executable(${test} ${test}.c)
  target_link_libraries(${test} check)
  target_link_libraries(${test} ${lib})
  add_test(NAME ${test} COMMAND ${test})
endmacro (do_test)

