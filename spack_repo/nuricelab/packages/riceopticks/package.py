# spack_repo/nuricelab/packages/laropticks/package.py
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# 1. First, explicitly import your base build class and GPU mixin
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

# 2. Then, import the general Spack Package API primitives
from spack.package import *

# 3. Define your class inheriting from both
class Riceopticks(CMakePackage, CudaPackage):
    """RiceOpticks: A framework built upon the original Opticks."""

    repo = "nuRiceLab/RiceOpticks"
    git = "https://github.com/%s" % repo
    version_patterns = ["v1.0r", "v1.0r"]

    version("main", branch="main", get_full_repo=True)

    variant("cxxstd", default="17", values=("11", "14", "17", "20"), multi=False, description="C++ standard")
    
    # externals (variants pinned by the larsoft env; geant4 must be +gdml)
    depends_on("cuda")
    depends_on("clhep")
    depends_on("geant4")
    depends_on("glew")
    depends_on("glfw")
    depends_on("glm")
    depends_on("glu")
    depends_on("nlohmann-json")
    depends_on("mesa")
    depends_on("optix-dev")
    depends_on("openssl")
    depends_on("plog")
    depends_on("python")

  
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

     #  THIS EXECUTING ONLY DURING A FRESH SOURCE BUILD
    
    def setup_build_environment(self, env):
        # When compiling from source, we feed the variables that 'opticks-full' 
        # or the CMake build relies on, dynamically derived from Spack dependencies.
        if "+cuda" in self.spec:
            cuda_root = self.spec["cuda"].prefix
            env.set("OPTICKS_CUDA_PREFIX", cuda_root)
            env.prepend_path("PATH", join_path(cuda_root, "bin"))
            env.prepend_path("LD_LIBRARY_PATH", join_path(cuda_root, "lib64"))
            env.prepend_path("CMAKE_PREFIX_PATH", cuda_root)

        if "optix" in self.spec:
            env.set("OPTICKS_OPTIX_PREFIX", self.spec["optix"].prefix)

        if "riceopticks" in self.spec:
            env.set("OPTICKS_PREFIX", self.spec["riceopticks"].prefix)


    # EXECUTES WHEN USERS RUN 'spack load riceopticks'
    
    def setup_run_environment(self, env):
        # 1. Point to your own compiled paths (your build folder artifacts)
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        # 2. Pass variables downstream so Opticks continues working at runtime
        if "+cuda" in self.spec:
            env.set("OPTICKS_CUDA_PREFIX", self.spec["cuda"].prefix)
        if "optix" in self.spec:
            env.set("OPTICKS_OPTIX_PREFIX", self.spec["optix"].prefix)
        if "opticks" in self.spec:
            env.set("OPTICKS_PREFIX", self.spec["opticks"].prefix)
