from conans import ConanFile, CMake 
import os
import multiprocessing
import inspect

class BoostHttpConan(ConanFile):
    name = "BoostHttp"
    version = "0.3"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/BoostGSoC14/boost.http.git"
    license = "Boost Software License 1.0"
    src_folder = "boost.http"
    install_folder = None

    def source(self):
        self.run( "git clone %s %s" %  (self.url, self.src_folder))
        self.run( "cd %s && git checkout -b v0.3 v0.3" % self.src_folder)

    def build(self):
        cmake = CMake( self.settings)
        self.install_folder = "%s/opt/" % self.conanfile_directory 
        self.run( 'cmake %s/%s %s -DCMAKE_INSTALL_PREFIX=%s' % ( 
            self.conanfile_directory, self.src_folder, cmake.command_line,
            self.install_folder))
        self.run( 'cmake --build . %s' % cmake.build_config)
        self.run( 'cmake --build . %s -- install' % cmake.build_config)

    def package(self):
        self.copy( pattern="libboost_http.*", dst="lib", src="%s/lib/" %
                self.install_folder)
        self.copy( pattern="*", dst="include", src="%s/include/" %
                self.install_folder) 

    def package_info(self):
        self.cpp_info.libs.extend(["boost_http", "boost_coroutine",
            "boost_system"])
