#!/usr/bin/env python3
"""A simple implementation of homework for kiwi.com machine learning weekend."""

__version_info__ = ('0', '1')
__version__ = '.'.join(__version_info__)
__title__ = 'ml_kiwi'
__author__ = 'Fridolin Pokorny'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Fridolin Pokorny'


from .lib import DataSource
from .lib import Defaults
from .lib import do_interpolate
from .lib import do_plot
from .utils import json_dump
from .errors import InputError
