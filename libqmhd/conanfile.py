from conans import ConanFile, CMake 
import os
import multiprocessing
import inspect

class libQMHDConan(ConanFile):
    name = "libqmhd"
    version = "0.1.0"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/fmiguelgarcia/libqmhd.git"
    license = "LGPL 2.0"
    requires = "libmicrohttpd/0.9.52@fmiguelgarcia/stable"
    generators = "qmake"
    src_folder = "libqmhd"

    def source(self):
        self.run( "git clone %s %s" %  (self.url, self.src_folder))

    def build(self):
        qmake_build_type = "release" if self.settings.build_type == "Release" else "debug"
        self.run( "cd %s && qmake CONFIG+=%s"
                % ( self.src_folder, qmake_build_type))
        self.run( "cd %s && make" % self.src_folder)

    def package(self):
        self.copy( pattern="libqmhd.*", dst="lib", src="%s/src" % self.src_folder)
        self.copy( pattern="*.h", dst="include", src="%s/src" % self.src_folder)

    def package_info(self):
        self.cpp_info.libs.extend(["qmhd"])
