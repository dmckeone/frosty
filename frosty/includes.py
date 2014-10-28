# -*- coding: utf-8 -*-
#
from __future__ import absolute_import

from warnings import warn

from .freezers import resolve_freezer


def _import_packages(packages, optional=None):
    """
    Get actual package references from an iterable of package names
    :param packages: iterable of package names
    :type packages: iter of basestr
    :return: set of package references
    :rtype: set
    """
    if not optional:
        optional = []

    package_references = set()

    # Check all reqiured packages
    failures = set()
    for package_name in packages:
        try:
            package_reference = __import__(package_name, globals(), locals(), [], 0)
            package_references.add(package_reference)
        except ImportError:
            failures.add(package_name)

    # Report aggregated list of import failures (save a developer time when building a new frozen environment)
    if failures:
        raise ImportError(u"Unable to find required packages: {0}".format(u", ".join(failures)))

    # Check all optional packages (and warn if some aren't found)
    failures = set()
    for package_name in optional:
        try:
            package_reference = __import__(package_name, globals(), locals(), [], 0)
            package_references.add(package_reference)
        except ImportError:
            failures.add(package_name)

    # Warn user which optional packages weren't found
    for failure in failures:
        warn(ImportWarning(u"Unable to import {0}".format(failure)))

    return package_references


def build_includes(include_packages, freezer=None, optional=None):
    """
    Iterate the list of packages to build a complete list of those packages as well as all subpackages.

    :param include_packages: list of package names
    :type: include_pacakges: list of basestr
    :param freezer: The freezer to use (See FREEZER constants)
    :param optional: Optional pacakge names to include (will only issue a warning if they don't exist)
    :return: complete set of package includes
    """
    freezer = resolve_freezer(freezer)

    # Import (or get reference to) all listed packages to ensure that they exist.
    package_references = _import_packages(include_packages, optional=optional)

    # Find all includes for the given freezer type
    includes = freezer.build_includes(package_references)

    return includes