# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDionysus(PythonPackage):
    """Library for computing persistent homology."""

    homepage = "https://www.mrzv.org/software/dionysus2"
    url      = "https://pypi.io/packages/source/d/dionysus/dionysus-2.0.6.tar.gz"
    git      = "https://github.com/mrzv/dionysus.git"

    version('2.0.6', sha256='cce43402c0ccde42f39f3aef773089eb66e47fec3671a5e72625027733697d21')
    version('master', branch='master')

    depends_on('cmake', type='build')
    depends_on('boost', type='build')
    depends_on('py-setuptools', type='build')
