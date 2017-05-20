from conans import ConanFile, CMake 
from conans.tools import get, chdir
import os
import shutil
import re
import fnmatch 

def withOptionToCmake( name, value):
    return "-D %s=%s " % (name ,("ON" if value else "OFF"))

class OpenCVConan(ConanFile):
    name = "OpenCV"
    version = "3.2.0"
    settings = "os", "compiler", "build_type", "arch"
    url = "http://opencv.org"
    license = "3-clause BSD License"
    description = "Open Source Computer Vision Library"
    generators = "cmake"
    options = { "opencv_with_ipp": [True, False],
            "opencv_with_qt": [True, False],
            "opencv_with_opengl": [True, False],
            "opencv_with_cuda": [True, False] }
    default_options = "opencv_with_ipp=False", \
        "opencv_with_qt=True", \
        "opencv_with_opengl=True", \
        "opencv_with_cuda=True"
    generated_libs = []

    def config(self):
        if self.settings.os == "Windows":
            self.settings.build_type = "Release"

    def source(self):
        build_path = "build"
        if not os.path.exists( build_path): 
            os.makedirs( build_path)
        with chdir( build_path):
            get( "https://github.com/opencv/opencv/archive/3.2.0.zip") 
            shutil.move( "opencv-3.2.0", "opencv")  

    def build(self):
        cmake = CMake( self)
        cmake.configure( 
            source_dir="opencv",
            build_dir="build",
            defs={
                "WITH_IPP": self.options.opencv_with_ipp,
                "WITH_QT": self.options.opencv_with_qt,
                "WITH_OPENGL": self.options.opencv_with_opengl,
                "WITH_CUDA": self.options.opencv_with_cuda,
                "CMAKE_INSTALL_PREFIX": "usr"
          })
        cmake.build()
        cmake.build(target="install")

    def package(self):
        install_prefix = "build/usr"
        self.copy( pattern="*", dst="lib", src="%s/lib" % install_prefix)
        self.copy( pattern="*", dst="bin", src="%s/bin" % install_prefix)
        self.copy( pattern="*", dst="include", src="%s/include" % install_prefix)
        self.copy( pattern="*", dst="shared", src="%s/shared" % install_prefix)
        self.copy( pattern="*", dst="etc", src="%s/etc" % install_prefix, keep_path=True)
        self.copy( pattern="*.dll", dst="lib", src=install_prefix, keep_path=False)
        self.copy( pattern="*.dll.a", dst="lib", src=install_prefix, keep_path=False)
        self.copy( pattern="*.exe", dst="lib", src=install_prefix, keep_path=False)
        filename_libs = []
        for root, dirnames, filenames in os.walk( install_prefix):
            for filename in fnmatch.filter( filenames, '*.dll'):
                filename_libs.append( filename)
            for filename in fnmatch.filter( filenames, '*.so'):
                filename_libs.append( filename)

        for libname in filename_libs:
            libname = re.sub( '^lib', '', libname)
            libname = re.sub( '\\.dll', '', libname)
            libname = re.sub( '\\.so', '', libname)
            self.generated_libs.append( libname) 
        self.output.info( "OpenCV generated libs: %s" % self.generated_libs )

    def package_info(self):
        self.cpp_info.libs.extend( self.generated_libs)
