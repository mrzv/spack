# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStringi(RPackage):
    """Allows for fast, correct, consistent, portable, as well as convenient
    character string/text processing in every locale and any native encoding.
    Owing to the use of the ICU library, the package provides R users with
    platform-independent functions known to Java, Perl, Python, PHP, and Ruby
    programmers. Among available features there are: pattern searching (e.g.,
    with ICU Java-like regular expressions or the Unicode Collation Algorithm),
    random string generation, case mapping, string transliteration,
    concatenation, Unicode normalization, date-time formatting and parsing,
    etc."""

    homepage = "http://www.gagolewski.com/software/stringi/"
    url      = "https://cran.r-project.org/src/contrib/stringi_1.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/stringi"

    version('1.1.5', '0d5ec30ae368ab1b87a36fee3e228e7b')
    version('1.1.3', '3b89cee3b5ef7c031077cd7707718e07')
    version('1.1.2', '0ec2faa62643e1900734c0eaf5096648')
    version('1.1.1', '32b919ee3fa8474530c4942962a6d8d9')

    depends_on('icu4c')
