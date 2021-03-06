from conans import ConanFile, CMake 
from conans.tools import get, chdir
import os
import shutil
import re

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
    #build_policy = "always"
    options = { "opencv_with_ipp": [True, False],
            "opencv_with_qt": [True, False],
            "opencv_with_opengl": [True, False],
            "opencv_with_cuda": [True, False] }
    default_options = "opencv_with_ipp=False", \
        "opencv_with_qt=True", \
        "opencv_with_opengl=True", \
        "opencv_with_cuda=True"

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
        self.copy( pattern="*", dst="include", src="%s/include" % install_prefix)
        self.copy( pattern="*", dst="etc", src="%s/etc" % install_prefix, keep_path=True)
        self.copy( pattern="*", dst="shared", src="%s/shared" % install_prefix)

        self.copy( pattern="**/opencv_*.lib", dst="lib", src=install_prefix, keep_path=False)
        self.copy( pattern="**/opencv_*.dll", dst="lib", src=install_prefix, keep_path=False)
        self.copy( pattern="*.exe", dst="bin", src=install_prefix, keep_path=False)

        self.copy( pattern="*.dll", dst="lib", src=install_prefix, keep_path=False)
        self.copy( pattern="*.dll.a", dst="lib", src=install_prefix, keep_path=False)

    def package_info(self):
        generated_libs = []
        libDir =  os.path.join( self.package_folder , "lib")
        for libname in os.listdir( libDir):
            if libname.endswith( ".lib"):
                libname = re.sub( '^lib', '', libname)
                libname = re.sub( '\\.dll', '', libname)
                libname = re.sub( '\\.so', '', libname)
                generated_libs.append( libname) 
        
        self.cpp_info.libs.extend( generated_libs)
