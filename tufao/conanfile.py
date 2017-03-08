from conans import ConanFile, CMake 
import os
import multiprocessing
import inspect

class TufaoConan(ConanFile):
    name = "Tufao"
    version = "1.4.1"
    settings = "os", "compiler", "build_type", "arch"
    requires = "BoostHttp/0.3@fmiguelgarcia/stable"
    url = "https://github.com/vinipsmaker/tufao.git"
    generators = "cmake"
    license = "LGPL v2"
    src_folder = "tufao"
    install_folder = None

    def source(self):
        self.run( "git clone %s %s" %  (self.url, self.src_folder))
        self.run( "cd %s && git checkout -b %s %s" % (self.src_folder,
            self.version, self.version))
        self.run( "cd %s && git submodule update --init" % self.src_folder) 
        self.addConanDep( "%s/src/CMakeLists.txt" % self.src_folder)

    def build(self):
        cmake = CMake( self.settings)
        self.run( 'cmake %s/%s %s' % ( 
            self.conanfile_directory, self.src_folder, cmake.command_line))
        self.run( 'cmake --build . %s' % cmake.build_config)
        
    def package(self):
        self.copy( pattern="**/libtufao1*", dst="lib", keep_path=False,
                links=True)
        self.copy( pattern="*.h", dst="include/Tufao", src="%s/src" % 
                self.src_folder)
        self.copy( pattern="*", dst="include/Tufao", src="%s/include" % 
                self.src_folder)

    def package_info(self):
        self.cpp_info.libs.extend(["tufao1"])

    def addConanDep(self, filePath):
        f = open( filePath, 'r+')
        lines = f.readlines()
        f.seek(0)
        f.write( 'include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n')
        f.write( "conan_basic_setup()\n")
        for line in lines:
            f.write( line)
        f.write( "target_link_libraries( ${TUFAO_LIBRARY} ${CONAN_LIBS})")
        f.close()

