#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
includes
----------------------------------
Test all freezer include functions
"""

from warnings import catch_warnings, simplefilter
from unittest import main as test_main
from unittest import TestCase

from frosty.includes import _import_packages, build_includes
from frosty.freezers import FREEZER


class Test_import_packages(TestCase):
    """
    All tests for the _import_packages internal function
    """

    def test_imports_exist(self):
        import wheel
        import sys
        expected = {wheel, sys}
        actual = _import_packages({u'wheel', u'sys'})
        self.assertSetEqual(expected, actual)

    def test_optional_imports_exist(self):
        import wheel
        import sys
        expected = {wheel, sys}
        actual = _import_packages({}, optional={u'wheel', u'sys'})
        self.assertSetEqual(expected, actual)

    def test_required_import_missing(self):
        try:
            import im_not_a_real_package  # Hopefully doesn't exist on a system
            raise EnvironmentError(u"Expected im_not_a_package to not exist, but it does!")
        except ImportError:
            pass

        with self.assertRaises(ImportError):
            _import_packages({u'im_not_a_real_package'})

    def test_optional_import_missing(self):
        try:
            import im_not_a_real_package  # Hopefully doesn't exist on a system
            raise EnvironmentError(u"Expected im_not_a_package to not exist, but it does!")
        except ImportError:
            pass

        with catch_warnings(record=True) as caught_warnings:
            simplefilter(u"always")
            _import_packages({}, optional={u'im_not_a_real_package'})

        self.assertEqual(len(caught_warnings), 1)
        self.assertTrue(all(w.category is ImportWarning for w in caught_warnings))


class Test_build_includes(TestCase):

    def test_default_build_includes(self):
        packages = {u'wheel', u'sys'}
        expected = {
            u'sys',
            u'wheel',
            u'wheel.signatures.*',
            u'wheel.test.*',
            u'wheel.test.complex-dist.complexdist.*',
            u'wheel.test.simple.dist.simpledist.*',
            u'wheel.tool.*',
        }
        actual = build_includes(packages, freezer=FREEZER.DEFAULT)
        self.assertSetEqual(expected, actual)

    def test_cxfreeze_build_includes(self):
        packages = {u'wheel', u'sys'}
        expected = {
            u'sys', u'wheel', u'wheel.__main__', u'wheel.archive', u'wheel.bdist_wheel', u'wheel.decorator',
            u'wheel.egg2wheel', u'wheel.install', u'wheel.metadata', u'wheel.paths', u'wheel.pep425tags',
            u'wheel.pkginfo', u'wheel.signatures', u'wheel.signatures.djbec', u'wheel.signatures.ed25519py',
            u'wheel.signatures.keys', u'wheel.test', u'wheel.test.complex-dist.complexdist',
            u'wheel.test.simple.dist.simpledist', u'wheel.test.test_basic', u'wheel.test.test_install',
            u'wheel.test.test_keys', u'wheel.test.test_paths', u'wheel.test.test_ranking',
            u'wheel.test.test_signatures', u'wheel.test.test_tagopt', u'wheel.test.test_tool',
            u'wheel.test.test_wheelfile', u'wheel.tool', u'wheel.util', u'wheel.wininst2wheel'
        }
        actual = build_includes(packages, freezer=FREEZER.CXFREEZE)
        print sorted(actual)
        self.assertSetEqual(expected, actual)

if __name__ == '__main__':
    test_main()