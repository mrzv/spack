# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Henson(CMakePackage):
    """Cooperative multitasking for in situ processing."""

    homepage = "https://github.com/mrzv/henson"
    url      = "https://github.com/mrzv/henson"
    git      = "https://github.com/mrzv/henson.git"

    version('master', branch='master')

    depends_on('mpi')

    variant('python', default=False, description= 'Build Python bindings')
    extends('python', when='+python')
    variant('mpi-wrappers', default=True, description= 'Build MPI wrappers (PMPI)')

    conflicts('^openmpi', when='+mpi-wrappers')

    def cmake_args(self):
        spec = self.spec
        args = []
        if '+python' in self.spec:
            args += ['-Dpython=on']
        else:
            args += ['-Dpython=off']

        if '+mpi-wrappers' in self.spec:
            args += ['-Dmpi-wrappers=on']
        else:
            args += ['-Dmpi-wrappers=off']

        return args
