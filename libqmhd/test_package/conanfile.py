from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "demo")

class OpenCVPackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libqmhd/0.1.0@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run( 'conan install %s' % self.conanfile_directory )
        self.run( 'cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run( "cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run(os.sep.join([".","bin", "packageTest"]))
