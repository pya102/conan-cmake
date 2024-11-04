from conan import ConanFile
import os

class CMakeConan(ConanFile):
    name = "cmake"
    version = "3.30.5"
    description = "CMake build system"
    license = "BSD-3-Clause"
    homepage = "https://cmake.org/"
    topics = ("cmake", "build", "system")
    settings = "os", "arch"
    package_type = "application"

    def source(self):
        self.run("git clone --branch v3.30.5 https://github.com/Kitware/CMake.git .")

    def build(self):
        # Ensure CMKAKE_MAKE_PROGRAM, CMAKE_C_COMPILER, and CMAKE_CXX_COMPILER are set
        self.make_program = "gmake"
        cc = os.getenv("CC", "gcc")
        cxx = os.getenv("CXX", "g++")

        self.output.info(f"Running bootstrap with prefix={self.package_folder}")

        # Clean the environment variables to avoid any conflicts
        env = os.environ.copy()
        env.pop("CMAKE_TOOLCHAIN_FILE", None) # Remove if set
        env.pop("CMAKE_PREFIX_PATH", None)    # Remove if set

        # Prepare the environment list for self.run()
        env_list = [f"{key}={value}" for key, value in env.items()]

        # Run the configure script directly
        self.run(f"./bootstrap "
                 f"--prefix={self.package_folder} "
                 f"-- -DCMAKE_MAKE_PROGRAM={self.make_program} "
                 f"-DCMAKE_C_COMPILER={cc} "
                 f"-DCMAKE_CXX_COMPILER={cxx}",
                 env=env_list # Pass the cleaned environment
                )


        # Run gmake with the appropriate number of processors
        self.run(f"{self.make_program} -j$(nproc)")

    def package(self):
        # Install the library files to the package folder
        self.run(f"{self.make_program} install")

    def package_info(self):
        # Specify the name of the library
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.bindirs = ["bin"]

        self.buildenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
