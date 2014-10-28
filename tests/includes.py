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
        import distutils
        import encodings
        import sys
        expected = {distutils, encodings, sys}
        actual = _import_packages({u'distutils', u'encodings', u'sys'})
        self.assertSetEqual(expected, actual)

    def test_optional_imports_exist(self):
        import distutils
        import encodings
        import sys
        expected = {distutils, encodings, sys}
        actual = _import_packages({}, optional={u'distutils', u'encodings', u'sys'})
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

    # Split out cx_freeze expected output because it's so large
    cx_freeze_expected = {
        u'distutils',
        u'distutils.archive_util',
        u'distutils.bcppcompiler',
        u'distutils.ccompiler',
        u'distutils.cmd',
        u'distutils.command',
        u'distutils.command.bdist',
        u'distutils.command.bdist_dumb',
        u'distutils.command.bdist_msi',
        u'distutils.command.bdist_rpm',
        u'distutils.command.bdist_wininst',
        u'distutils.command.build',
        u'distutils.command.build_clib',
        u'distutils.command.build_ext',
        u'distutils.command.build_py',
        u'distutils.command.build_scripts',
        u'distutils.command.check',
        u'distutils.command.clean',
        u'distutils.command.config',
        u'distutils.command.install',
        u'distutils.command.install_data',
        u'distutils.command.install_egg_info',
        u'distutils.command.install_headers',
        u'distutils.command.install_lib',
        u'distutils.command.install_scripts',
        u'distutils.command.register',
        u'distutils.command.sdist',
        u'distutils.command.upload',
        u'distutils.config',
        u'distutils.core',
        u'distutils.cygwinccompiler',
        u'distutils.debug',
        u'distutils.dep_util',
        u'distutils.dir_util',
        u'distutils.dist',
        u'distutils.emxccompiler',
        u'distutils.errors',
        u'distutils.extension',
        u'distutils.fancy_getopt',
        u'distutils.file_util',
        u'distutils.filelist',
        u'distutils.log',
        u'distutils.msvc9compiler',
        u'distutils.msvccompiler',
        u'distutils.spawn',
        u'distutils.sysconfig',
        u'distutils.tests',
        u'distutils.tests.setuptools_build_ext',
        u'distutils.tests.setuptools_extension',
        u'distutils.tests.support',
        u'distutils.tests.test_archive_util',
        u'distutils.tests.test_bdist',
        u'distutils.tests.test_bdist_dumb',
        u'distutils.tests.test_bdist_msi',
        u'distutils.tests.test_bdist_rpm',
        u'distutils.tests.test_bdist_wininst',
        u'distutils.tests.test_build',
        u'distutils.tests.test_build_clib',
        u'distutils.tests.test_build_ext',
        u'distutils.tests.test_build_py',
        u'distutils.tests.test_build_scripts',
        u'distutils.tests.test_ccompiler',
        u'distutils.tests.test_check',
        u'distutils.tests.test_clean',
        u'distutils.tests.test_cmd',
        u'distutils.tests.test_config',
        u'distutils.tests.test_config_cmd',
        u'distutils.tests.test_core',
        u'distutils.tests.test_dep_util',
        u'distutils.tests.test_dir_util',
        u'distutils.tests.test_dist',
        u'distutils.tests.test_file_util',
        u'distutils.tests.test_filelist',
        u'distutils.tests.test_install',
        u'distutils.tests.test_install_data',
        u'distutils.tests.test_install_headers',
        u'distutils.tests.test_install_lib',
        u'distutils.tests.test_install_scripts',
        u'distutils.tests.test_msvc9compiler',
        u'distutils.tests.test_register',
        u'distutils.tests.test_sdist',
        u'distutils.tests.test_spawn',
        u'distutils.tests.test_sysconfig',
        u'distutils.tests.test_text_file',
        u'distutils.tests.test_unixccompiler',
        u'distutils.tests.test_upload',
        u'distutils.tests.test_util',
        u'distutils.tests.test_version',
        u'distutils.tests.test_versionpredicate',
        u'distutils.text_file',
        u'distutils.unixccompiler',
        u'distutils.util',
        u'distutils.version',
        u'distutils.versionpredicate',
        u'sys'
    }

    def test_default_build_includes(self):
        packages = {u'distutils', u'encodings', u'sys'}
        expected = {
            u'distutils',
            u'distutils.command.*',
            u'distutils.tests.*',
            u'encodings',
            u'sys'
        }
        actual = build_includes(packages, freezer=FREEZER.DEFAULT)
        self.assertSetEqual(expected, actual)

    def test_cxfreeze_build_includes(self):
        packages = {u'distutils', u'sys'}
        expected = self.cx_freeze_expected
        actual = build_includes(packages, freezer=FREEZER.CXFREEZE)
        self.assertSetEqual(expected, actual)

if __name__ == '__main__':
    test_main()