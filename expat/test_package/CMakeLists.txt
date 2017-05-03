project(LibQMHDTest)
cmake_minimum_required(VERSION 3.0.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable( packageTest main.cpp)
target_link_libraries( packageTest ${CONAN_LIBS})

set_property( TARGET packageTest  PROPERTY CXX_STANDARD 11)
set_property( TARGET packageTest APPEND_STRING PROPERTY COMPILE_FLAGS "-Wall -std=c++11")
