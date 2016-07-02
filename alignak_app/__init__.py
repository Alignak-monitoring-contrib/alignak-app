#!/usr/bin/env python
# -*- codinf: utf-8 -*-

"""
    Alignak App

    This module is an Alignak App Indicator
"""
# Application version and manifest
VERSION = (0, 2, 0)

__version__ = '.'.join((str(each) for each in VERSION[:4]))

from alignak_app import alignak_data, application
