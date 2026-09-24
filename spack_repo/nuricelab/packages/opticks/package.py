# spack_repo/nuricelab/packages/laropticks/package.py
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# 1. First, explicitly import your base build class and GPU mixin
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

# 2. Then, import the general Spack Package API primitives
from spack.package import *

# 3. Define your class inheriting from both
class Opticks(CMakePackage, CudaPackage):
    """Opticks: A GPU Accelerated Optical Photon Simulation using NVIDIA OptiX 7+"""

    repo = "simoncblyth/opticks"
    git = "https://github.com/%s" % repo
    version_patterns = ["v0.7.1", "v0.7.0","v0.6.9","v0.6.8"]
    maintainers("ilkerparmaksiz")

    version("latest", branch="master", get_full_repo=True)
    version("0.7.1", tag="v0.7.1", preferred=True)
    version("0.7.0", tag="v0.7.0")
    version("0.6.9", tag="v0.6.9") 
    
    variant("cxxstd", default="17", values=("11", "14", "17", "20"), multi=False, description="C++ standard")
    
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cuda")
    depends_on("clhep")
    depends_on("geant4")
    depends_on("optix-dev") 
    depends_on("python")
    def cmake(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass
  
    def install(self, spec, prefix):
        env["OPTICKS_HOME"] = str(self.stage.source_path)
        env["OPTICKS_PREFIX"] = str(prefix)
        env["OPTICKS_CUDA_PREFIX"] = str(spec["cuda"].prefix)
        env["OPTICKS_OPTIX_PREFIX"] = str(spec["optix-dev"].prefix)

        bash = which("bash", required=True)

        setup_script = join_path(
            self.stage.source_path,
            "opticks.bash"
        )
        bash(
              "-c",
              f'''
              source "{setup_script}"
              export OPTICKS_CONFIG=Release
              opticks-env
              echo "----------------------------"
              echo OPTICKS_HOME: $OPTICKS_HOME
              echo OPTICKS_PREFIX: $OPTICKS_PREFIX
              echo OPTICKS_CUDA_PREFIX: $OPTICKS_CUDA_PREFIX
              echo OPTICKS_OPTIX_PREFIX: $OPTICKS_OPTIX_PREFIX
              echo "----------------------------"
              opticks-full
              '''
            )
    def setup_run_environment(self, env):
        env.set("OPTICKS_PREFIX", self.prefix)

        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        #env.prepend_path("PATH", join_path(self.prefix, "lib"))

        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        #env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib64"))

        if "cuda" in self.spec:
            env.set("OPTICKS_CUDA_PREFIX", self.spec["cuda"].prefix)

        if "optix-dev" in self.spec:
            env.set("OPTICKS_OPTIX_PREFIX", self.spec["optix-dev"].prefix)
