from conans import ConanFile, CMake, tools
import shutil
import os 

class KF5ECMConan(ConanFile):
    # Conan 
    name = "KF5_ECM"
    version = "5.36.0"
    description = ""
    license = "http://opensource.org/licenses/BSD-3-Clause"
    url = "https://api.kde.org/ecm"
    settings = "os", "compiler", "build_type", "arch"
    options = { "qt_version": "ANY" }
    default_options = ""


    def configure(self):
        self.options.qt_version = os.popen("qmake -query QT_VERSION").read().strip()
        self.output.info("Configure Qt Version: %s" % self.options.qt_version)

    def source(self):
        self.run( "git clone git://anongit.kde.org/extra-cmake-modules")
        with tools.chdir( "extra-cmake-modules"):
            self.run( "git checkout -b %s v%s" % (self.version, self.version))

    def build(self):
        cmake = CMake( self)
        cmake.configure( source_dir="extra-cmake-modules")
        cmake.build()
        
    def package(self):
        self.copy( pattern="*.h", src="qxmpp/src/base", dst="include/", keep_path=True)
        self.copy( pattern="*.h", src="qxmpp/src/client", dst="include/", keep_path=True)
        self.copy( pattern="*.h", src="qxmpp/src/server", dst="include/", keep_path=True)
        if self.settings.compiler == "Visual Studio":
            for lib_ext in [ "dll", "pdb", "exp", "lib"]:
                self.copy( pattern="qxmpp*.%s" % lib_ext, src="qxmpp/src", dst="lib/", keep_path=False, symlinks=True)
        else:
            self.copy( pattern="*qxmpp*.so*", src="qxmpp/src", dst="lib/", keep_path=False, symlinks=True)

    def package_info(self):
        lib_name = "qxmpp" if self.settings.build_type == "Release" else "qxmpp_d"
        if self.settings.compiler == "Visual Studio":
            lib_name += "0"
        self.cpp_info.libs.extend([lib_name])

