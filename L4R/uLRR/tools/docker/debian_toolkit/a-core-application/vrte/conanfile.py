from conans import ConanFile, CMake, tools


class LogDltLibConan(ConanFile):
    name = "L4R-VRTE"
    version = "1.0.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Hello here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake","CMakeToolchain", "virtualenv", "virtualrunenv", "cmake_paths"
    vrte_version = "r22-08"

    def requirements(self):
        self.requires(f"log-dlt-lib/{self.vrte_version}@vrte-ci/baselines") 