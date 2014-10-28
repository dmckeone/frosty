#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1.1'

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read()
test_requirements = []

setup(
    name='frosty',
    version=VERSION,
    description='Frosty is a collection of utilities for working with frozen packages.',
    long_description=readme + '\n\n' + history,
    author='David McKeone',
    author_email='davidmckeone@gmail.com',
    url='https://github.com/dmckeone/frosty',
    packages=[
        'frosty',
    ],
    package_dir={
        'frosty': 'frosty'
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    download_url = 'https://github.com/dmckeone/Frosty/tarball/{}'.format(VERSION),
    keywords=['frosty', 'frozen', 'esky', 'py2app', 'py2exe', 'bbfreeze', 'cxfreeze', 'utilities'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)