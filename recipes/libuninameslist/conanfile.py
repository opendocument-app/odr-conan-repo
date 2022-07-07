from conans import ConanFile, tools, AutoToolsBuildEnvironment

required_conan_version = ">=1.33.0"


class LibuninameslistConan(ConanFile):
    name = "libuninameslist"
    version = "20211114"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/fontforge/libuninameslist/"
    description = "A library with a large (sparse) array mapping each unicode code point to the annotation data for it provided in http://www.unicode.org/Public/UNIDATA/NamesList.txt"
    topics = "unicode"
    license = "GPL-2.0"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    build_requires = ["autoconf/2.71", "automake/1.16.4", "libtool/2.4.6"]

    exports_sources = ["CMakeLists.txt"]
    generators = "cmake", "cmake_find_package"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(url="https://github.com/fontforge/libuninameslist/archive/refs/tags/20211114.tar.gz",
                  sha1="5550669f9dc278d9536b20cc25f8cf9769e13ba2",
                  destination=self._source_subfolder, strip_root=True)

    def _patch_sources(self):
        pass

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools

        with tools.chdir(self._source_subfolder):
            self.run("autoreconf -fiv", run_environment=True)

        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args = ["--enable-static=yes", "--enable-shared=no"] if not self.options.shared else ["--enable-static=no", "--enable-shared=yes"]
        self._autotools.configure(args=args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()
 
    def package(self):
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
