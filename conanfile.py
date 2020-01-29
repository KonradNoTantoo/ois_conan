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
    folder_name = "OIS-{}".format(version)

    def requirements(self):
        if tools.os_info.is_linux:
            self.requires("libx11/1.6.8@bincrafters/stable")

    def source(self):
        tools.get("https://github.com/wgois/OIS/archive/v{}.tar.gz".format(self.version))

        tools.replace_in_file(os.path.join(self.folder_name, "CMakeLists.txt"),
            "project(OIS)",
            '''PROJECT(OIS)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.folder_name)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ois_d" if self.settings.build_type == "Debug" else "ois"]
        self.cpp_info.includedirs = [os.path.join("include", "ois")]
