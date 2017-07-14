from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "demo")

class OpenCVPackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "KF5_KArchive/5.36.0@%s/%s" % (username, channel)
    generators = "cmake"
    options = { "qt_version": "ANY" }
    default_options = ""

    def configure(self):
        self.options.qt_version = os.popen("qmake -query QT_VERSION").read().strip()
        self.output.info("Configure Qt Version: %s" % self.options.qt_version)

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run(os.sep.join([".","bin", "packageTest"]))
