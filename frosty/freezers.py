# -*- coding: utf-8 -*-
#
from __future__ import absolute_import

import os
import re
import six

from warnings import warn

from .compat import UnicodeMixin


class _Default(UnicodeMixin, object):
    """
    Default strategy that should be mostly compatible with all freezers. "Ya gotta start somewhere."

    Although freezers should generally not require a custom class (patches welcome!), if one was going to create
    their own freezer, then this would be the class to inherit from.
    """
    @classmethod
    def _split_packages(cls, include_packages):
        """
        Split an iterable of packages into packages that need to be passed through, and those that need to have their
        disk location resolved.

        Some modules don't have a '__file__' attribute.  AFAIK these aren't packages, so they can just be passed
        through to the includes as-is
        :return: 2-tuple of a list of the pass-through includes and the package_root_paths
        """
        passthrough_includes = set([
            six.text_type(package.__name__)
            for package in include_packages
            if not hasattr(package, '__file__')
        ])
        package_file_paths = dict([
            (six.text_type(os.path.abspath(package.__file__)), six.text_type(package.__name__))
            for package in include_packages
            if hasattr(package, '__file__')
        ])
        return passthrough_includes, package_file_paths

    @classmethod
    def build_includes(cls, include_packages):
        """
        The default include strategy is to add a star (*) wild card after all sub-packages (but not the main package).
        This strategy is compatible with py2app and bbfreeze.

        Example (From SaltStack 2014.7):

            salt
            salt.fileserver.*
            salt.modules.*
            etc...

        :param include_packages: List of package references to recurse for subpackages
        """
        includes, package_root_paths = cls._split_packages(include_packages)
        for package_path, package_name in six.iteritems(package_root_paths):
            if re.search(r'__init__.py.*$', package_path):
                # Looks like a package.  Walk the directory and see if there are more.
                package_files = set([os.path.dirname(package_path)])
                for root, dirs, files in os.walk(os.path.dirname(package_path)):
                    if '__init__.py' in files:
                        package_files.add(root)

                if len(package_files) > 1:
                    common_prefix = os.path.commonprefix(package_files)
                    common_dir = os.path.dirname(common_prefix)
                    package_tails = set([f[len(common_dir) + len(os.sep):] for f in package_files])
                    package_names = set([tail.replace(os.sep, '.') for tail in package_tails])
                    package_names_with_star = set([pkg + '.*' if pkg != package_name else pkg for pkg in package_names])
                    includes |= package_names_with_star

                else:
                    # No sub-packages.  Just add the package name by itself.
                    includes.add(package_name)
            else:
                # Not a package.  Just add the module.
                includes.add(package_name)

        return includes

    def __unicode__(self):
        return u"default"

    def __repr__(self):
        return u"Default "


class _Py2Exe(_Default):
    """
    Specific implementations for py2exe (http://www.py2exe.org/)
    """
    def __unicode__(self):
        return u"py2exe"


class _BbFreeze(_Default):
    """
    Specific implementations for bbfreeze (https://pypi.python.org/pypi/bbfreeze/)
    """
    def __unicode__(self):
        return u"bbfreeze"


class _Py2App(_Default):
    """
    Specific implementations for py2app (http://pythonhosted.org//py2app/)
    """
    def __unicode__(self):
        return u"py2app"


class _CxFreeze(_Default):
    """
    Specific implementations for cx_freeze (http://cx-freeze.sourceforge.net/)
    """
    @classmethod
    def build_includes(cls, include_packages):
        """
        cx_freeze doesn't support the star (*) method of sub-module inclusion, so all submodules must be included
        explicitly.

        Example (From SaltStack 2014.7):

            salt
            salt.fileserver
            salt.fileserver.gitfs
            salt.fileserver.hgfs
            salt.fileserver.minionfs
            salt.fileserver.roots
            etc...

        :param include_packages: List of package references to recurse for subpackages
        """
        includes, package_root_paths = cls._split_packages(include_packages)
        for package_path, package_name in six.iteritems(package_root_paths):
            includes.add(package_name)
            if re.search(r'__init__.py.*$', package_path):
                # Looks like a package.  Walk the directory and see if there are more.
                package_modules = set()
                for root, dirs, files in os.walk(os.path.dirname(package_path)):
                    if '__init__.py' in files:
                        package_modules.add(root)
                        for module in [f for f in files if f != u"__init__.py" and f.endswith('.py')]:
                            package_modules.add(os.path.join(root, module))

                common_prefix = os.path.commonprefix(package_modules)
                common_dir = os.path.dirname(common_prefix)
                package_tails = set([f[len(common_dir) + len(os.sep):] for f in package_modules])
                package_names = set([os.path.splitext(tail)[0].replace(os.sep, '.') for tail in package_tails])
                includes |= package_names
        return includes

    def __unicode__(self):
        return u"cxfreeze"


class FREEZER(object):
    """
    Constants for selecting appropriate freezers (All resolve to string names if used with str() or unicode())
    """

    DEFAULT = _Default
    PY2EXE = _Py2Exe
    PY2APP = _Py2App
    BBFREEZE = _BbFreeze
    CXFREEZE = _CxFreeze

    ALL = set([DEFAULT, PY2EXE, PY2APP, BBFREEZE, CXFREEZE])


def _freezer_lookup(freezer_string):
    """
    Translate a string that may be a freezer name into the internal freezer constant

    :param freezer_string
    :return:
    """
    sanitized = freezer_string.lower().strip()
    for freezer in FREEZER.ALL:
        freezer_instance = freezer()
        freezer_name = six.text_type(freezer_instance)
        if freezer_name == six.text_type(sanitized):
            return freezer
    else:
        if sanitized != freezer_string:
            raise ValueError(u"Unsupported freezer type \"{0}\". (Sanitized to \"{1}\")".format(freezer_string,
                                                                                              sanitized))
        else:
            raise ValueError(u"Unsupported freezer type \"{0}\".".format(freezer_string))


def resolve_freezer(freezer):
    """
    Locate the appropriate freezer given FREEZER or string input from the programmer.

    :param freezer: FREEZER constant or string for the freezer that is requested.  (None = FREEZER.DEFAULT)
    :return:
    """
    # Set default freezer if there was none
    if not freezer:
        return _Default()

    # Allow character based lookups as well
    if isinstance(freezer, six.string_types):
        cls = _freezer_lookup(freezer)
        return cls()

    # Allow plain class definition lookups (we instantiate the class)
    if freezer.__class__ == type.__class__:
        return freezer()

    # Warn when a custom freezer implementation is used.
    if freezer not in FREEZER.ALL:
        warn(u"Using custom freezer implelmentation: {0}".format(freezer))

    return freezer





