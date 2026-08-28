# spack_repo/nuricelab/packages/opticks/package.py
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# RiceOpticks builds project-by-project (om.bash / opticks-full), not via a
# single CMake project. Fill install() from your container-stack build.
# The parts marked REQUIRED are what laropticks / MPD actually need.

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package


class RiceOpticks(Package):
    """RiceOpticks: GPU optical photon simulation (OptiX/CUDA)."""

    homepage = "https://github.com/nuRiceLab/RiceOpticks"
    git = "https://github.com/nuRiceLab/RiceOpticks.git"

    # REQUIRED: a 'develop' version so `spack info opticks` lists it.
    version("develop", branch="main", get_full_repo=True)

    variant("cxxstd", default="17", values=("17", "20"), multi=False)

    depends_on("cmake", type="build")
    depends_on("cuda@13:")
    depends_on("geant4")
    depends_on("clhep")
    depends_on("boost")
    # OptiX is proprietary / non-redistributable — declare it external in
    # packages.yaml, then uncomment:
    # depends_on("optix")

    def install(self, spec, prefix):
        # TODO: drive RiceOpticks' own build with CMAKE_INSTALL_PREFIX=prefix
        # so these config packages land under <prefix>:
        #   G4CXConfig.cmake, U4Config.cmake, PLogConfig.cmake, ...
        raise InstallError("Fill in the RiceOpticks build from the container recipe")

    # REQUIRED so laropticks' find_package(G4CX/U4 CONFIG) + find_dependency(PLog)
    # and its $ENV{OPTICKS_HOME}/$ENV{OPTICKS_PREFIX} usage resolve.
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("OPTICKS_HOME", self.prefix)
        env.set("OPTICKS_PREFIX", self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)

    def setup_run_environment(self, env):
        env.set("OPTICKS_HOME", self.prefix)
        env.set("OPTICKS_PREFIX", self.prefix)
