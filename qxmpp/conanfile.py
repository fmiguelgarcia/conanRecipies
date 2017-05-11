from conans import ConanFile, CMake 
from conans.tools import os_info, get, patch
import shutil
import os 

class QXmppConan(ConanFile):
    # Conan 
    name = "QXmpp"
    version = "0.9.3"
    description = "QXmpp is a cross-platform C++ XMPP client and server library"
    license = "LGPL 2.1"
    url = "http://doc.qxmpp.org"
    settings = "os", "compiler", "build_type", "arch"

    # Other
    source_path = "qxmpp"

    def source(self):
        # Get source code
        get("https://github.com/fmiguelgarcia/qxmpp/archive/v0.9.3.zip")
        shutil.move( "qxmpp-0.9.3", self.source_path)

    def build(self):
        self.run( "cd build && qmake "

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
