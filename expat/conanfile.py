import os
from conans import ConanFile, CMake
from conans.tools import get, patch
import shutil

class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.0"
    license = "MIT"
    url = "http://expat.sourceforge.net"
    description = '''Expat is an XML parser library written in C. 
        It is a stream-oriented parser in which an application registers handlers 
        for things the parser might find in the XML document (like start tags). 
        An introductory article (http://www.xml.com/pub/1999/09/expat/index.html) on 
        using Expat is available on xml.com.
    '''
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    exports = "patches/*"

    def source(self):
        # Get source code
        get( "https://github.com/libexpat/libexpat/archive/R_2_2_0.zip")
        shutil.move( "libexpat-R_2_2_0", "libexpat")

        # Apply patches
        self.output.info( "Applying patches in source code")
        patch( base_path="libexpat/expat", patch_file="patches/00_CMakeLists.txt.diff")

        
    def build(self):
        expat_source_dir = os.path.abspath( "libexpat/expat") 
        expat_build_dir = os.sep.join( [expat_source_dir, "build"])
        
        cmake = CMake( self)
        cmake.definitions["BUILD_tools"] = "OFF"
        cmake.definitions["BUILD_shared"] = "ON"
        cmake.definitions["BUILD_examples"] = "OFF" 
        cmake.definitions["BUILD_tests"] = "OFF" 
        cmake.definitions["BUILD_doc"] = "OFF" 
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install" 
        cmake.configure( source_dir=expat_source_dir, build_dir=expat_build_dir )
        cmake.build( target="install")

    def package(self):
        self.copy( pattern="*.h", src="libexpat/expat/build/install/include", dst="include", keep_path=True)
        self.copy( pattern="libexpat.*", src="libexpat/expat/build/install/lib", dst="lib", keep_path=False)
        self.copy( pattern="libexpat.*", src="libexpat/expat/build/install/bin", dst="lib", keep_path=False)
        # Windwos in debug mode
        self.copy( pattern="libexpatd.*", src="libexpat/expat/build/install/lib", dst="lib", keep_path=False)
        self.copy( pattern="libexpatd.*", src="libexpat/expat/build/install/bin", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs.extend(["expatd"])
        else:
            self.cpp_info.libs.extend(["expat"])
    
