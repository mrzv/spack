# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Compiz(AutotoolsPackage):
    """compiz - OpenGL window and compositing manager.

    Compiz is an OpenGL compositing manager that use
    GLX_EXT_texture_from_pixmap for binding redirected top-level
    windows to texture objects. It has a flexible plug-in system
    and it is designed to run well on most graphics hardware."""

    homepage = "http://www.compiz.org/"
    url      = "https://www.x.org/archive/individual/app/compiz-0.7.8.tar.gz"

    version('0.7.8', 'e99977d9170a7bd5d571004eed038428')

    depends_on('libxcb')
    depends_on('libxcomposite')
    depends_on('libxfixes')
    depends_on('libxdamage')
    depends_on('libxrandr')
    depends_on('libxinerama')
    depends_on('libice')
    depends_on('libsm')
    depends_on('libxml2')
    depends_on('libxslt')

    # TODO: add dependencies
    # libstartup-notification-1.0 >= 0.7
    depends_on('libxrender')
    depends_on('libpng')
    depends_on('glib')
    depends_on('gconf')
