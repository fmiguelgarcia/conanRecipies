from conans import ConanFile, CMake 
import os
import multiprocessing
import inspect

class TelepathyQtConan(ConanFile):
    name = "Telepathy-Qt"
    version = "0.9.7"
    description = "Qt high-level binding for Telepathy"
    settings = "os", "compiler", "build_type", "arch"
    url = "git://anongit.freedesktop.org/telepathy/telepathy-qt"
    generators = "cmake"
    src_folder = "telepathy-qt"
    options = {
            "with_farstream": [True, False],
            "with_test": [True, False],
            "with_examples": [True, False]
    }
    default_options = "with_farstream=False", "with_test=False", "with_examples=False"

    def source(self):
        gitTag = "telepathy-qt-%s" % self.version
        self.run( "git clone %s %s" %  (self.url, self.src_folder))
        self.run( "cd %s && git checkout -b %s %s" % (self.src_folder,
            gitTag, gitTag))

    def build(self):
        cmake = CMake( self.settings)
        cmake_options = { 
            "CMAKE_INSTALL_PREFIX": "install",
            "ENABLE_FARSTREAM": self.options.with_farstream,
            "ENABLE_TESTS": self.options.with_test,
            "ENABLE_EXAMPLES": self.options.with_examples
        }
        cmake.configure( self, defs=cmake_options, source_dir=self.src_folder)
        cmake.build( self, target="install")
        
    def package(self):
        self.copy( pattern="*", dst="include", 
            src = os.path.join( "install", "include"), keep_path=True)
        self.copy( pattern="**/libtelepathy-qt5*", dst="lib", keep_path=False,
                links=True)

    def package_info(self):
        self.cpp_info.libs.extend(["telepathy-qt5", "telepathy-qt5-service"])
        self.cpp_info.includedirs.extend(["include/telepathy-qt5"])

