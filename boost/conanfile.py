from conans import ConanFile
from conans.tools import download, unzip
import os
import shutil

class BoostQtConan(ConanFile):
    name = "Boost"
    version = "1.64.0"
    description = "Boost (HEADERS Only) provides free peer-reviewed portable C++ source libraries"
    url = "http://www.boost.org"
    generators = "cmake"
    license = "http://www.boost.org/users/license.html"

    def source(self):
        zip_name = "boost_1_64_0.zip"
        download( "https://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.zip", zip_name)
        unzip( zip_name)

        # We are going to use only header files
        shutil.move( "boost_1_64_0/boost", ".")
        # Remove unused files
        shutil.rmtree( "boost_1_64_0")
        os.unlink( zip_name)

    def package(self):
        self.copy( pattern="*", dst="include/boost", 
            src = "boost", keep_path=True)

