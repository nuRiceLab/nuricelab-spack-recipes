# spack_repo/nuricelab/packages/laropticks/package.py
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Laropticks(CMakePackage, FnalGithubPackage):
    """LArSoft module for GPU optical-photon propagation via RiceOpticks."""

    repo = "nuRiceLab/laropticks"
    git = "https://github.com/%s" % repo
    version_patterns = ["v10_09_01", "10.09.01"]

    # MPD requires a 'develop' version to exist. Point it at the branch you
    # develop from; you can still `git checkout` any branch in the srcs area.
    version("develop", branch="spack", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cetmodules", type="build")

    # art / cet suite
    depends_on("art")
    depends_on("art-root-io")
    depends_on("artg4tk")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("messagefacility")

    # LArSoft
    depends_on("larcore")
    depends_on("larcorealg")
    depends_on("lardata")
    depends_on("lardataobj")
    depends_on("larg4")
    depends_on("larsim")
    depends_on("larsoft-data")
    depends_on("nurandom")
    depends_on("nusimdata")

    # externals (variants pinned by the larsoft env; geant4 must be +gdml)
    depends_on("clhep")
    depends_on("geant4")
    depends_on("root")
    depends_on("range-v3")

    # GPU optical simulation
    # depends_on("opticks")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
        return (flags, None, None)

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", prefix.job)
        env.prepend_path("FW_SEARCH_PATH", prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", prefix.gdml)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)
