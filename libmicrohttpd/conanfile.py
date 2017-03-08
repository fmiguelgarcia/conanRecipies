from conans import ConanFile, CMake 
import os
import multiprocessing
import inspect

class MicroHTTPDVConan(ConanFile):
    name = "libmicrohttpd"
    version = "0.9.52"
    settings = {"os":["Linux"], "compiler": None, "build_type": None, "arch": None }
    url = "https://gnunet.org/git/libmicrohttpd.git"
    license = "LGPL 2.0"
    src_folder = None
    install_folder = None

    def source(self):
        self.src_folder = "%s/%s" %  (os.getcwd(), self.name)
        self.install_folder = "%s/usr/local" % self.src_folder
        self.output.info("Prefix install path: %s" % self.install_folder)

        self.run( "git clone %s %s" %  (self.url, self.src_folder))

    def build(self):
        os.chdir( self.src_folder)
        self.run( "autoreconf -fi" )
        self.run( "./configure --prefix=%s" % self.install_folder)
        self.run( "make -j%d" % multiprocessing.cpu_count())
        self.run( "make install")

    def package(self):
        self.copy( pattern="*", dst="lib", src="%s/lib" % self.install_folder)
        self.copy( pattern="*.h", dst="include/microhttpd", src="%s/include" % self.install_folder )
        self.copy( pattern="*", dst="share", src="%s/share" % self.install_folder)

    def package_info(self):
        self.cpp_info.libs.extend(["microhttpd"])
        self.cpp_info.includedirs.extend( ["include/microhttpd"])

