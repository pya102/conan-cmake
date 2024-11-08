from conans import ConanFile, tools
import os

class CMakeConan(ConanFile):
    name = "cmake"
    version = "3.30.5"
    description = "CMake build system"
    license = "BSD-3-Clause"
    homepage = "https://cmake.org/"
    topics = ("cmake", "build", "system")
    settings = "os", "arch"

    def source(self):
        self.run("git clone --branch v3.30.5 https://github.com/Kitware/CMake.git .")

    def build(self):
        # Ensure CMAKE_MAKE_PROGRAM, CMAKE_C_COMPILER, and CMAKE_CXX_COMPILER are set
        make_program = "gmake"
        cc = os.getenv("CC", "gcc")
        cxx = os.getenv("CXX", "g++")

        self.output.info(f"Running bootstrap with prefix={self.package_folder}")

        # Clean the environment variables to avoid any conflicts
        env = os.environ.copy()
        env.pop("CMAKE_TOOLCHAIN_FILE", None)  # Remove if set
        env.pop("CMAKE_PREFIX_PATH", None)     # Remove if set

        # Prepare the environment list for self.run()
        with tools.environment_append(env):
            # Run the configure script directly
            self.run(f"./bootstrap "
                     f"--prefix={self.package_folder} "
                     f"-- -DCMAKE_MAKE_PROGRAM={make_program} "
                     f"-DCMAKE_C_COMPILER={cc} "
                     f"-DCMAKE_CXX_COMPILER={cxx}")

            # Run gmake with the appropriate number of processors
            self.run(f"{make_program} -j{tools.cpu_count()}")

    def package(self):
        # Install the library files to the package folder
        self.run("gmake install")

    def package_info(self):
        # Specify the name of the library
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.bindirs = ["bin"]

        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
