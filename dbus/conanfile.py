from conans import ConanFile, CMake 
from conans.tools import os_info, get, patch
import shutil
import os 

class DBusConan(ConanFile):
    name = "dbus"
    version = "1.10.18"
    description = "D-Bus framework."
    license = "LGPL 2.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "expat/2.2.0@fmiguelgarcia/stable"
    exports = ["patches/*"]

    def source(self):
        # Get source code
        get("https://dbus.freedesktop.org/releases/dbus/dbus-1.10.18.tar.gz")
        shutil.move( "dbus-1.10.18", "dbus")

        # Apply patches
        self.output.info( "Applying patches in source code")
        patch( base_path="dbus/cmake", patch_file="patches/00_CMakeLists.txt.diff")

    def build(self):
        cmake = CMake( self)
        cmake_dir = os.sep.join( [ self.conanfile_directory, "dbus", "cmake"]) 
        cmake.definitions["DBUS_BUILD_TESTS"] = "OFF"        
        cmake.definitions["CONAN_DISABLE_CHECK_COMPILER"] = "ON"        
        cmake.definitions["CMAKE_CXX_COMPILER"] = self.settings.compiler        
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install" 
        cmake.configure( source_dir=cmake_dir, build_dir="build")
        cmake.build( target="install")

    def package(self):
        self.copy( pattern="*.h", src="build/install/include", dst="include/", keep_path=True)
        self.copy( pattern="libdbus*", src="build/install/bin", dst="lib/", keep_path=False)
        self.copy( pattern="libdbus*", src="build/install/lib", dst="lib/", keep_path=False)
        self.copy( pattern="dbus-*.exe", src="build/install/bin", dst="bin/", keep_path=False)
        self.copy( pattern="dbus-*.bat", src="build/install/bin", dst="bin/", keep_path=False)
        self.copy( pattern="*", src="build/install/share", dst="share/", keep_path=True)
        self.copy( pattern="*", src="build/install/etc", dst="etc/", keep_path=True)

    def package_info(self):
        self.cpp_info.libs.extend(["libtelepathy-qt5"])
