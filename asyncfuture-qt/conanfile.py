from conans import ConanFile
import os
import multiprocessing
import inspect

class AsyncFutureQtConan(ConanFile):
    name = "AsyncFuture-Qt"
    version = "0.3.2"
    description = "Use QFuture like a Promise object"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/benlau/asyncfuture.git"
    generators = "cmake", "ycm"
    license = "Apache 2.0"
    src_folder = "asyncFutureQt"

    def source(self):
        gitTag = "qpm/%s" % self.version
        self.run( "git clone %s %s" %  (self.url, self.src_folder))
        self.run( "cd %s && git checkout -b %s %s" % (self.src_folder,
            gitTag, gitTag))

    # def build(self):
        
    def package(self):
        self.copy( pattern="*.h", dst="include" )

