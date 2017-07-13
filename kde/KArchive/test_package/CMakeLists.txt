project(PackageTest)
cmake_minimum_required(VERSION 3.0.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable( packageTest main.cpp)
target_link_libraries( packageTest ${CONAN_LIBS})
target_compile_features( packageTest PUBLIC cxx_nullptr)
