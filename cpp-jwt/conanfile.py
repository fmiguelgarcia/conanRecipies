from conans import ConanFile, tools 

class CPPJWTConan(ConanFile):
    name = "cpp-jwt"
    version = "1.1.1"
    description = 'A C++14 library for JSON Web Tokens'
    url = "https://github.com/arun11299/cpp-jwt"
    generators = "cmake"
    license = "MIT"
    no_copy_source = True

    def source(self):
        tools.get( "https://github.com/arun11299/cpp-jwt/archive/v1.1.1.zip",
                md5='f1956e7bb52950b13e33de99abf4c0be')

    def package_id(self):
        self.info.header_only()

    def package(self):
        self.copy( pattern="**/*.hpp", dst="include",
                src="cpp-jwt-1.1.1/include/", keep_path=True, links=True)
        self.copy( pattern="**/*.ipp", dst="include",
                src="cpp-jwt-1.1.1/include/", keep_path=True, links=True)

