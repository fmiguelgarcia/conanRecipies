project(PackageTest)
cmake_minimum_required(VERSION 3.0.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable( packageTest example.c)
target_link_libraries( packageTest  ${CONAN_LIBS})
set_property( TARGET packageTest  PROPERTY CXX_STANDARD 11)
