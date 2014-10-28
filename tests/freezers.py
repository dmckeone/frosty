#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
freezers
----------------------------------
Test all freezer lookup helper functions
"""
from __future__ import absolute_import

import six
import sys

if sys.version_info <= (2, 6, 0, 'final', 0):
    import unittest2 as unittest
else:
    import unittest

from frosty.freezers import FREEZER, resolve_freezer


class Test_freezer_resolve(unittest.TestCase):
    """
    All tests for the _import_packages internal function
    """

    freezers = [
        (FREEZER.DEFAULT, 'default'),
        (FREEZER.PY2APP, 'py2app'),
        (FREEZER.PY2EXE, 'py2exe'),
        (FREEZER.BBFREEZE, 'bbfreeze'),
        (FREEZER.CXFREEZE, 'cxfreeze')
    ]

    def test_string_constant_lookup(self):
        """
        Ensure that a freezer can be lookup up via the string constants
        """
        for expected_cls, lookup_string in self.freezers:
            actual_instance = resolve_freezer(lookup_string)
            actual_cls = actual_instance.__class__
            self.assertEqual(actual_cls, expected_cls)

    def test_python_constant_lookup(self):
        """
        Ensure that a freezer can be lookup up via the FREEZER constant
        """
        for python_constant_cls, expected_name in self.freezers:
            actual_instance = resolve_freezer(python_constant_cls)
            actual_name = six.text_type(actual_instance)
            self.assertEqual(actual_name, expected_name)

    def test_instantiated_built_in_lookup(self):
        """
        Ensure that an instantiated freezer is passed through
        """
        actual_instance = resolve_freezer(FREEZER.DEFAULT())
        self.assertEqual(actual_instance.__class__, FREEZER.DEFAULT)


if __name__ == '__main__':
    unittest.main()