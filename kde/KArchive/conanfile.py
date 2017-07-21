from conans import ConanFile, CMake, tools
import os

class KF5KArchiveConan(ConanFile):
    # Conan 
    name = "KF5_KArchive"
    version = "5.36.0"
    description = "KArchive provides classes for easy reading, creation and manipulation of 'archive' formats like ZIP and TAR."
    requires = "KF5_ECM/5.36.0@fmiguelgarcia/stable", "zlib/1.2.11@conan/stable"
    license = "http://opensource.org/licenses/BSD-3-Clause"
    url = "https://api.kde.org/frameworks/karchive/html/index.html"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = { 
        "qt_version": "ANY",
        "zip_support": [True, False],
        "bzip2_support" : [True, False],
        "lzma_support" : [True, False]
    }
    default_options = "zip_support=True", \
            "bzip2_support=False", \
            "lzma_support=False"

    def configure(self):
        self.options.qt_version = os.popen("qmake -query QT_VERSION").read().strip()
        self.output.info("Configure Qt Version: %s" % self.options.qt_version)
        # Check BZip2 and l
        self.options.bzip2_support = self.find_package("BZIP2")
        self.options.lzma_support = self.find_package("LibLZMA")
        self.output.info("Compression algorithms supported: ZIP(True), BZIP2({}), LZMA({})".format( self.options.bzip2_support, self.options.lzma_support)) 

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
            "CMAKE_INSTALL_PREFIX": "install" 
        }
        cmake = CMake( self)
        cmake.configure( source_dir="karchive", defs=cmake_defs)
        cmake.build()
        cmake.build( target="install")
        
    def package(self):
        self.copy( pattern="*", src="install/include", dst="include", keep_path=True, symlinks=True)
        if tools.os_info.is_windows:
            self.copy( pattern="*.dll", src="install/bin", dst="bin", keep_path=True, symlinks=True)
            self.copy( pattern="*.lib", src="install/bin", dst="lib", keep_path=True, symlinks=True)
        elif tools.os_info.is_linux:
            self.copy( pattern="**KF5Archive.so*", src="install/lib", dst="lib", keep_path=False, symlinks=True)

    def package_info(self):
        self.cpp_info.libs = ["KF5Archive"]
        self.cpp_info.includedirs.append( "include/KF5/KArchive")

    def find_package(self, package):
        isPackageFound = None

        # Link compiler info from Conan to CMake

        # Find package with cmake
        try:
            self.run( "cmake --find-package -DNAME=%s -DCOMPILER_ID=GNU -DLANGUAGE=CXX -DMODE=EXIST" % package)
            isPackageFound = True
        except:
            isPackageFound = False

        return isPackageFound



