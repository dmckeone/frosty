# -*- coding: utf-8 -*-
#
from __future__ import absolute_import

import six
import sys

from contextlib import contextmanager


class UnicodeMixin(object):
    """
    Mixin for keeping Python 3 compatibility with the models
    """
    if sys.version_info >= (3, 0, 0, 'final', 0):
        __str__ = lambda x: x.__unicode__()
    else:
        __str__ = lambda x: six.text_type(x).encode('utf-8')


class ReprMixin(object):
    """
    Mixin for keeping Python 3 compatibility with the models
    """
    if sys.version_info >= (3, 0, 0, 'final', 0):
        __repr__ = lambda x: x.__unicode__()
    else:
        __repr__ = lambda x: six.text_type(x).encode('utf-8')


if sys.version_info < (3, 4, 0, 'final', 0):
    @contextmanager
    def ignored(*exceptions):
        """
        Ignore all exceptions within the scope of a context manager.

        Example:

            >>>filename = "/tmp/does_not_exist.txt"
            >>>with ignored(OSError, IOError):
            >>>    os.remove(filename)
        """
        try:
            yield
        except exceptions:
            pass