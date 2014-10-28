#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
includes
----------------------------------
Test all freezer include functions
"""
from __future__ import absolute_import

import unittest

from warnings import catch_warnings, simplefilter

from frosty.includes import _import_packages, build_includes
from frosty.freezers import FREEZER


class Test_import_packages(unittest.TestCase):
    """
    All tests for the _import_packages internal function
    """

    def test_imports_exist(self):
        import wheel
        import sys
        expected = set([wheel, sys])
        actual = _import_packages(set(['wheel', 'sys']))
        self.assertEqual(expected, actual)

    def test_optional_imports_exist(self):
        import wheel
        import sys
        expected = set([wheel, sys])
        actual = _import_packages(set(), optional=set(['wheel', 'sys']))
        self.assertEqual(expected, actual)

    def test_required_import_missing(self):
        try:
            import im_not_a_real_package  # Hopefully doesn't exist on a system
            raise EnvironmentError(u"Expected im_not_a_package to not exist, but it does!")
        except ImportError:
            pass

        def test_import_package():
            _import_packages(set(['im_not_a_real_package']))
        self.assertRaises(ImportError, test_import_package)

    def test_optional_import_missing(self):
        try:
            import im_not_a_real_package  # Hopefully doesn't exist on a system
            raise EnvironmentError(u"Expected im_not_a_package to not exist, but it does!")
        except ImportError:
            pass

        with catch_warnings(record=True) as caught_warnings:
            simplefilter(u"always")
            _import_packages(set(), optional=set(['im_not_a_real_package']))

        self.assertEqual(len(caught_warnings), 1)
        self.assertTrue(all(w.category is ImportWarning for w in caught_warnings))


class Test_build_includes(unittest.TestCase):

    def test_default_build_includes(self):
        packages = set(['wheel', 'sys'])
        expected = set([
            'sys',
            'wheel',
            'wheel.signatures.*',
            'wheel.test.*',
            'wheel.test.complex-dist.complexdist.*',
            'wheel.test.simple.dist.simpledist.*',
            'wheel.tool.*',
        ])
        actual = build_includes(packages, freezer=FREEZER.DEFAULT)
        self.assertEqual(expected, actual)

    def test_cxfreeze_build_includes(self):
        packages = set(['wheel', 'sys'])
        expected = set([
            'sys', 'wheel', 'wheel.__main__', 'wheel.archive', 'wheel.bdist_wheel', 'wheel.decorator',
            'wheel.egg2wheel', 'wheel.install', 'wheel.metadata', 'wheel.paths', 'wheel.pep425tags',
            'wheel.pkginfo', 'wheel.signatures', 'wheel.signatures.djbec', 'wheel.signatures.ed25519py',
            'wheel.signatures.keys', 'wheel.test', 'wheel.test.complex-dist.complexdist',
            'wheel.test.simple.dist.simpledist', 'wheel.test.test_basic', 'wheel.test.test_install',
            'wheel.test.test_keys', 'wheel.test.test_paths', 'wheel.test.test_ranking',
            'wheel.test.test_signatures', 'wheel.test.test_tagopt', 'wheel.test.test_tool',
            'wheel.test.test_wheelfile', 'wheel.tool', 'wheel.util', 'wheel.wininst2wheel'
        ])
        actual = build_includes(packages, freezer=FREEZER.CXFREEZE)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()