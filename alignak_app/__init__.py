#!/usr/bin/env python
# -*- codinf: utf-8 -*-

"""
    Alignak App

    This module is an Alignak App Indicator
"""

# Application version and manifest
VERSION = (0, 2, 0)
__application__ = u"Alignak-App"
__short_version__ = '.'.join((str(each) for each in VERSION[:2]))
__version__ = '.'.join((str(each) for each in VERSION[:4]))
__author__ = u"Estrada Matthieu"
__copyright__ = u"2015-2016 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__description__ = u"Alignak monitoring application AppIndicator"
__releasenotes__ = u"""Alignak monitoring application AppIndicator"""
__doc_url__ = "https://github.com/Alignak-monitoring-contrib/alignak-app"

# Application Manifest
manifest = {
    'name': __application__,
    'version': __version__,
    'author': __author__,
    'description': __description__,
    'copyright': __copyright__,
    'license': __license__,
    'release': __releasenotes__,
    'doc': __doc_url__
}
