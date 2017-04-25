from conans import ConanFile, CMake 
from conans.tools import download, unzip
import os
import shutil
import re
import multiprocessing
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
    src_folder = "opencv"
    options = { "opencv_with_ipp": [True, False],
            "opencv_with_qt": [True, False],
            "opencv_with_opengl": [True, False],
            "opencv_with_cuda": [True, False] }
    default_options = "opencv_with_ipp=False", \
        "opencv_with_qt=True", \
        "opencv_with_opengl=True", \
        "opencv_with_cuda=True"
    cmake_build_path = None
    absolute_build_path = None
    generated_libs = []

    def config(self):
        if self.settings.os == "Windows":
            self.settings.build_type = "Release"

    def source(self):
        zip_name = "3.2.0.zip"
        download( "https://github.com/opencv/opencv/archive/3.2.0.zip", zip_name) 
        unzip( zip_name)
        os.unlink( zip_name)
        shutil.move( "opencv-3.2.0", self.src_folder)  

    def build(self):
        cmake = CMake( self.settings)
        relative_build_path = "%s/build" % self.src_folder
        self.absolute_build_path = "%s/%s" % (os.getcwd(), relative_build_path)

        with_ipp = withOptionToCmake( "WITH_IPP", self.options.opencv_with_ipp)
        with_qt = withOptionToCmake( "WITH_QT", self.options.opencv_with_qt)
        with_opengl = withOptionToCmake( "WITH_OPENGL", self.options.opencv_with_opengl)
        with_cuda = withOptionToCmake( "WITH_CUDA", self.options.opencv_with_cuda)
        cmake_install_prefix = "-D CMAKE_INSTALL_PREFIX:PATH=%s/usr " % self.absolute_build_path
        cmake_ext = cmake_install_prefix + with_ipp + with_qt + with_opengl + with_cuda

        os.makedirs( relative_build_path)
        os.chdir( relative_build_path)
        self.run( "cmake %s %s .."
                % ( cmake_ext, cmake.command_line))
        self.run("cmake --build . %s -- -j %d"
                % ( cmake.build_config, multiprocessing.cpu_count()))
        self.run("cmake --build . --target install %s"
                % cmake.build_config)

    def package(self):
        install_prefix = "%s/usr" % self.absolute_build_path
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

    def package_info(self):
        self.cpp_info.libs.extend( self.generated_libs)
