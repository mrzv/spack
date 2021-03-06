# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from __future__ import division

import argparse
import cgi
import fnmatch
import re
import sys
import math

from six import StringIO

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.dependency
import spack.repo
import spack.cmd.common.arguments as arguments

description = "list and search available packages"
section = "basic"
level = "short"


formatters = {}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results')
    subparser.add_argument(
        '-d', '--search-description', action='store_true', default=False,
        help='filtering will also search the description for a match')
    subparser.add_argument(
        '--format', default='name_only', choices=formatters,
        help='format to be used to print the output [default: name_only]')

    arguments.add_common_arguments(subparser, ['tags'])


def filter_by_name(pkgs, args):
    """
    Filters the sequence of packages according to user prescriptions

    Args:
        pkgs: sequence of packages
        args: parsed command line arguments

    Returns:
        filtered and sorted list of packages
    """
    if args.filter:
        res = []
        for f in args.filter:
            if '*' not in f and '?' not in f:
                r = fnmatch.translate('*' + f + '*')
            else:
                r = fnmatch.translate(f)

            rc = re.compile(r, flags=re.IGNORECASE)
            res.append(rc)

        if args.search_description:
            def match(p, f):
                if f.match(p):
                    return True

                pkg = spack.repo.get(p)
                if pkg.__doc__:
                    return f.match(pkg.__doc__)
                return False
        else:
            def match(p, f):
                return f.match(p)
        pkgs = [p for p in pkgs if any(match(p, f) for f in res)]

    return sorted(pkgs, key=lambda s: s.lower())


@formatter
def name_only(pkgs):
    indent = 0
    if sys.stdout.isatty():
        tty.msg("%d packages." % len(pkgs))
    colify(pkgs, indent=indent)


def github_url(pkg):
    """Link to a package file on github."""
    url = 'https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/{0}/package.py'
    return url.format(pkg.name)


def rst_table(elts):
    """Print out a RST-style table."""
    cols = StringIO()
    ncol, widths = colify(elts, output=cols, tty=True)
    header = ' '.join('=' * (w - 1) for w in widths)
    return '%s\n%s%s' % (header, cols.getvalue(), header)


def rows_for_ncols(elts, ncols):
    """Print out rows in a table with ncols of elts laid out vertically."""
    clen = int(math.ceil(len(elts) / ncols))
    for r in range(clen):
        row = []
        for c in range(ncols):
            i = c * clen + r
            row.append(elts[i] if i < len(elts) else None)
        yield row


@formatter
def rst(pkg_names):
    """Print out information on all packages in restructured text."""

    pkgs = [spack.repo.get(name) for name in pkg_names]

    print('.. _package-list:')
    print()
    print('============')
    print('Package List')
    print('============')
    print()
    print('This is a list of things you can install using Spack.  It is')
    print('automatically generated based on the packages in the latest Spack')
    print('release.')
    print()
    print('Spack currently has %d mainline packages:' % len(pkgs))
    print()
    print(rst_table('`%s`_' % p for p in pkg_names))
    print()

    # Output some text for each package.
    for pkg in pkgs:
        print('-----')
        print()
        print('.. _%s:' % pkg.name)
        print()
        # Must be at least 2 long, breaks for single letter packages like R.
        print('-' * max(len(pkg.name), 2))
        print(pkg.name)
        print('-' * max(len(pkg.name), 2))
        print()
        print('Homepage:')
        print('  * `%s <%s>`__' % (cgi.escape(pkg.homepage), pkg.homepage))
        print()
        print('Spack package:')
        print('  * `%s/package.py <%s>`__' % (pkg.name, github_url(pkg)))
        print()
        if pkg.versions:
            print('Versions:')
            print('  ' + ', '.join(str(v) for v in
                                   reversed(sorted(pkg.versions))))
            print()

        for deptype in spack.dependency.all_deptypes:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                print('%s Dependencies' % deptype.capitalize())
                print('  ' + ', '.join('%s_' % d if d in pkg_names
                                       else d for d in deps))
                print()

        print('Description:')
        print(pkg.format_doc(indent=2))
        print()


@formatter
def html(pkg_names):
    """Print out information on all packages in Sphinx HTML.

    This is intended to be inlined directly into Sphinx documentation.
    We write HTML instead of RST for speed; generating RST from *all*
    packages causes the Sphinx build to take forever. Including this as
    raw HTML is much faster.
    """

    # Read in all packages
    pkgs = [spack.repo.get(name) for name in pkg_names]

    # Start at 2 because the title of the page from Sphinx is id1.
    span_id = 2

    # HTML header with an increasing id span
    def head(n, span_id, title, anchor=None):
        if anchor is None:
            anchor = title
        print(('<span id="id%d"></span>'
               '<h1>%s<a class="headerlink" href="#%s" '
               'title="Permalink to this headline">&para;</a>'
               '</h1>') % (span_id, title, anchor))

    # Start with the number of packages, skipping the title and intro
    # blurb, which we maintain in the RST file.
    print('<p>')
    print('Spack currently has %d mainline packages:' % len(pkgs))
    print('</p>')

    # Table of links to all packages
    print('<table border="1" class="docutils">')
    print('<tbody valign="top">')
    for i, row in enumerate(rows_for_ncols(pkg_names, 3)):
        print('<tr class="row-odd">' if i % 2 == 0 else
              '<tr class="row-even">')
        for name in row:
            print('<td>')
            print('<a class="reference internal" href="#%s">%s</a></td>'
                  % (name, name))
            print('</td>')
        print('</tr>')
    print('</tbody>')
    print('</table>')
    print('<hr class="docutils"/>')

    # Output some text for each package.
    for pkg in pkgs:
        print('<div class="section" id="%s">' % pkg.name)
        head(2, span_id, pkg.name)
        span_id += 1

        print('<dl class="docutils">')

        print('<dt>Homepage:</dt>')
        print('<dd><ul class="first last simple">')
        print(('<li>'
               '<a class="reference external" href="%s">%s</a>'
               '</li>') % (pkg.homepage, cgi.escape(pkg.homepage)))
        print('</ul></dd>')

        print('<dt>Spack package:</dt>')
        print('<dd><ul class="first last simple">')
        print(('<li>'
               '<a class="reference external" href="%s">%s/package.py</a>'
               '</li>') % (github_url(pkg), pkg.name))
        print('</ul></dd>')

        if pkg.versions:
            print('<dt>Versions:</dt>')
            print('<dd>')
            print(', '.join(str(v) for v in reversed(sorted(pkg.versions))))
            print('</dd>')

        for deptype in spack.dependency.all_deptypes:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                print('<dt>%s Dependencies:</dt>' % deptype.capitalize())
                print('<dd>')
                print(', '.join(
                    d if d not in pkg_names else
                    '<a class="reference internal" href="#%s">%s</a>' % (d, d)
                    for d in deps))
                print('</dd>')

        print('<dt>Description:</dt>')
        print('<dd>')
        print(cgi.escape(pkg.format_doc(indent=2)))
        print('</dd>')
        print('</dl>')

        print('<hr class="docutils"/>')
        print('</div>')


def list(parser, args):
    # Retrieve the names of all the packages
    pkgs = set(spack.repo.all_package_names())
    # Filter the set appropriately
    sorted_packages = filter_by_name(pkgs, args)

    # Filter by tags
    if args.tags:
        packages_with_tags = set(
            spack.repo.path.packages_with_tags(*args.tags))
        sorted_packages = set(sorted_packages) & packages_with_tags
        sorted_packages = sorted(sorted_packages)

    # Print to stdout
    formatters[args.format](sorted_packages)
