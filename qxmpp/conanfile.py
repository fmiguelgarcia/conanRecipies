from conans import ConanFile, tools
import shutil

class QXmppConan(ConanFile):
    # Conan 
    name = "QXmpp"
    version = "0.9.3"
    description = "QXmpp is a cross-platform C++ XMPP client and server library"
    license = "LGPL 2.1"
    url = "http://doc.qxmpp.org"
    settings = "os", "compiler", "build_type", "arch"
    options = { "use_doxygen":[True, False],
        "use_opus": [True,False],
        "use_speex": [True,False],
        "use_theora": [True,False],
        "autotest_internal": [True,False],
        "use_vpx": [True,False] }
    default_options = "use_doxygen=False", \
        "use_opus=False", \
        "use_speex=False", \
        "use_theora=False", \
        "autotest_internal=True", \
        "use_vpx=False"

    # Other
    source_path = "qxmpp"
    prefix = "usr"

    def source(self):
        # Get source code
        tools.get("https://github.com/fmiguelgarcia/qxmpp/archive/v0.9.3.zip")
        shutil.move( "qxmpp-0.9.3", self.source_path)

    def build(self):
        qmake_options = "CONFIG+=debug " if self.settings.build_type == "Debug" else "CONFIG+=release "
        qmake_options += "CONFIG+=warn_on " 
        qmake_options += "QXMPP_AUTOTEST_INTERNAL=1 " if self.options.autotest_internal else ""
        qmake_options += "QXMPP_USE_DOXYGEN=1 " if self.options.use_doxygen else ""
        qmake_options += "QXMPP_USE_OPUS=1 " if self.options.use_opus else ""
        qmake_options += "QXMPP_USE_SPEEX=1 " if self.options.use_speex else ""
        qmake_options += "QXMPP_USE_THEORA=1 " if self.options.use_theora else ""
        qmake_options += "QXMPP_USE_VPX=1 " if self.options.use_vpx else ""
        
        with tools.chdir( "qxmpp"):
            self.run( "qmake \"%s\"" % qmake_options)

            if self.settings.compiler == "Visual Studio":
                with tools.environment_append( {"CL": "/MP"}):
                    self.run( "nmake")
            else:
                self.run( "make -j %d" % tools.cpu_count())

    def package(self):
        self.copy( pattern="*.h", src="qxmpp/src/base", dst="include/", keep_path=True)
        self.copy( pattern="*.h", src="qxmpp/src/client", dst="include/", keep_path=True)
        self.copy( pattern="*.h", src="qxmpp/src/server", dst="include/", keep_path=True)
        if self.settings.compiler == "Visual Studio":
            for lib_ext in [ "dll", "pdb", "exp", "lib"]:
                self.copy( pattern="qxmpp*.%s" % lib_ext, src="qxmpp/src", dst="lib/", keep_path=False, symlinks=True)
        else:
            self.copy( pattern="*qxmpp.so*", src="qxmpp/src", dst="lib/", keep_path=False, symlinks=True)

    def package_info(self):
        lib_name = "qxmpp"
        if self.settings.compiler == "Visual Studio":
            lib_name = "qxmpp0" if self.settings.build_type == "Release" else "qxmpp_d0"
        self.cpp_info.libs.extend([lib_name])

