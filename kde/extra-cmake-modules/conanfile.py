from conans import ConanFile, CMake, tools

class KF5ECMConan(ConanFile):
    # Conan 
    name = "KF5_ECM"
    version = "5.36.0"
    description = "Extra CMake Modules for KF5"
    license = "http://opensource.org/licenses/BSD-3-Clause"
    url = "https://api.kde.org/ecm"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports =  "ECMConfig.cmake", "ECMConfigVersion.cmake"

    def source(self):
        self.run( "git clone git://anongit.kde.org/extra-cmake-modules")
        with tools.chdir( "extra-cmake-modules"):
            self.run( "git checkout -b %s v%s" % (self.version, self.version))

    def build(self):
        cmake_defs = { 
            "CMAKE_INSTALL_PREFIX": "install" 
        }
        cmake = CMake( self)
        cmake.configure( source_dir="../extra-cmake-modules", build_dir="build", defs=cmake_defs)
        cmake.build()
        cmake.build( target="install")
        
    def package(self):
        self.copy( pattern="ECMConfig.cmake", keep_path=True )
        self.copy( pattern="ECMConfigVersion.cmake", keep_path=True )
        self.copy( pattern="*", src="build/install", keep_path=True, symlinks=True)

    def package_info(self):
        self.cpp_info.resdirs = ["share"]
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

