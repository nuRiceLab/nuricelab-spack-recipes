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
    version_patterns = ["v1.0r", "v1.0r"]
    maintainers("ilkerparmaksiz","ahiguera-mx")
    # MPD requires a 'develop' version to exist. Point it at the branch you
    # develop from; you can still `git checkout` any branch in the srcs area.
    version("latest", branch="main", get_full_repo=True)
    version("develop", branch="develop", get_full_repo=True)
    version("v1_0r", tag="v1_0r")

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
    depends_on("larana", type="run")	
    # externals (variants pinned by the larsoft env; geant4 must be +gdml)
    depends_on("clhep")
    depends_on("geant4")
    depends_on("root")
    depends_on("range-v3")

    # GPU optical simulation
    depends_on("riceopticks")
   
    # DUNE Specific
    depends_on("dunesw",type="run")
    depends_on("dunecore",type="run")
    depends_on("duneopdet", type="run")
    depends_on("dunesim", type="run")
    depends_on("dunepdlegacy", type="run")
    depends_on("dunedataprep", type="run")
    depends_on("dunecalib", type="run")
    depends_on("duneprototypes", type="run")   
    depends_on("dunereco", type="run")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
        return (flags, None, None)

    #@sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", join_path(self.prefix, "fcl"))
        env.prepend_path("FW_SEARCH_PATH", prefix.gdml)

    #@sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", join_path(self.prefix, "fcl"))
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)
        env.set("GEOM", "PDFullSimOpticks")
        env.set("OPTICKS_MAX_PHOTON", "80000000")
        env.set("OPTICKS_MAX_SLOT", "80000000")
        env.set("OPTICKS_EVENT_SKIPAHEAD", "80000000")
        env.set("OPTICKS_PROPAGATE_EPSILON", "0.01")
        env.set("OPTICKS_PROPAGATE_EPSILON0", "0")
        env.set("OPTICKS_MAX_BOUNCE", "100")
        env.set("OPTICKS_INTEGRATION_MODE", "1") # 1 GPU ONLY, 2 CPU ONLY, and 3 Both CPU and GPU
        env.set("OPTICKS_EVENT_MODE", "Minimal")
        env.set("CUDA_VISIBLE_DEVICES", "0")
        env.set("OPTICKS_START_INDEX", "0")
        env.set("SProf__WRITE", "0")

