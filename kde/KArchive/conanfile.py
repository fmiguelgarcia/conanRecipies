from conans import ConanFile, CMake, tools
import os

class KF5KArchiveConan(ConanFile):
    # Conan 
    name = "KF5_KArchive"
    version = "5.36.0"
    description = "KArchive provides classes for easy reading, creation and manipulation of 'archive' formats like ZIP and TAR."
    requires = "KF5_ECM/5.36.0@fmiguelgarcia/stable"
    license = "http://opensource.org/licenses/BSD-3-Clause"
    url = "https://api.kde.org/frameworks/karchive/html/index.html"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = { "qt_version": "ANY" }
    default_options = ""

    def configure(self):
        self.options.qt_version = os.popen("qmake -query QT_VERSION").read().strip()
        self.output.info("Configure Qt Version: %s" % self.options.qt_version)

    def source(self):
        self.run( "git clone git://anongit.kde.org/karchive.git")
        with tools.chdir( "karchive"):
            self.run( "git checkout -b %s v%s" % (self.version, self.version))
            tools.replace_in_file( 
                "CMakeLists.txt",
                "project(KArchive VERSION ${KF5_VERSION})",
                '''project(KArchive VERSION ${KF5_VERSION})
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake_defs = { 
            "CMAKE_INSTALL_PREFIX": "%s/install" % self.build_folder
        }
        cmake = CMake( self)
        cmake.configure( source_dir="karchive", defs=cmake_defs)
        cmake.build()
        cmake.build( target="install")
        
    def package(self):
        self.copy( pattern="*", src="%s/install" % self.build_folder, keep_path=True)

    def package_info(self):
        self.cpp_info.resdirs = ["share"]
        self.env_info.x = ""

