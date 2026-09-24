# spack_repo/nuricelab/packages/laropticks/package.py
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Standalone(CMakePackage):
    """LArSoft module for GPU optical-photon propagation via RiceOpticks."""

    repo = "nuRiceLab/OpticalSims"
    git = "https://github.com/%s" % repo
    version_patterns = ["latest", "develop","demo","v1.0"]
    maintainers("ilkerparmaksiz")
    # MPD requires a 'develop' version to exist. Point it at the branch you
    # develop from; you can still `git checkout` any branch in the srcs area.
    version("latest", branch="master", get_full_repo=True)
    version("develop", branch="develop", get_full_repo=True)
    version("demo", branch="demo", get_full_repo=True)
    version("v1.0", tag="v1.0")

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    # externals (variants pinned by the larsoft env; geant4 must be +gdml)
    depends_on("geant4")
    depends_on("root")
    # GPU optical simulation
    depends_on("riceopticks")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
                self.define("With_Opticks", True)]  # Or use define_from_variant if you have a variant for it]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
        return (flags, None, None)

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)
                
    @run_after('install')
    def install_extra_data(self):
        # This runs AFTER 'make install' has already compiled 
        # and installed your binaries into prefix.bin
        install_tree("GDML", str(self.prefix.GDML))
        install_tree("macros",str(self.prefix.macros))  
    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.set("GDML_DIR", self.prefix.GDML)
        env.set("MACRO_DIR", self.prefix.macros)
        env.set("GEOM", "Test")
        env.set("OPTICKS_MAX_PHOTON", "20000000")
        env.set("OPTICKS_MAX_SLOT", "20000000")
        env.set("OPTICKS_EVENT_SKIPAHEAD", "20000000")
        env.set("OPTICKS_PROPAGATE_EPSILON", "0.01")
        env.set("OPTICKS_PROPAGATE_EPSILON0", "0")
        env.set("OPTICKS_MAX_BOUNCE", "100")
        env.set("OPTICKS_INTEGRATION_MODE", "3")
        env.set("OPTICKS_EVENT_MODE", "Minimal")
        env.set("CUDA_VISIBLE_DEVICES", "0")
        env.set("OPTICKS_START_INDEX", "0")
        env.set("SProf__WRITE", "0")

