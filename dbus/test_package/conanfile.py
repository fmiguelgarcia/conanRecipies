from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "demo")

class PackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "dbus/1.10.18@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build() 

    def test(self):
        self.run(os.sep.join([".","bin", "packageTest"]))
