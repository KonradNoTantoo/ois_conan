from conans import ConanFile, CMake, tools
import os


class OisConan(ConanFile):
    name = "ois"
    version = "1.5"
    license = "zlib"
    author = "konrad.no.tantoo"
    url = "https://github.com/KonradNoTantoo/ois_conan"
    description = "Cross Platform Object Oriented Input Lib System. Meant to be very robust and compatible with many systems and operating systems."
    topics = ("User input", "UI")
    settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False]}
    # default_options = "shared=False"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get("https://github.com/wgois/OIS/archive/v{}.tar.gz".format(self.version))
        os.rename("OIS-{}".format(self.version), self._source_subfolder)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "project(OIS)",
            '''PROJECT(OIS)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ois_d" if self.settings.build_type == "Debug" else "ois"]
        self.cpp_info.includedirs = [os.path.join("include", "ois")]
