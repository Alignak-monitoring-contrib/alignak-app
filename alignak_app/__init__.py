#!/usr/bin/env python
# -*- codinf: utf-8 -*-

# Copyright (c) 2015-2016:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

"""
    Alignak App

    This module is an appindicator for Alignak.

    Application notify you when you have hosts / services DOWN.
    You'll be notified on your desktop and you can reach your Hosts and Services on your WebUI
    from this application.
"""

from logging import getLogger
from alignak_app.utils import create_logger

logger = getLogger(__name__)

create_logger(logger)

# Application version and manifest
VERSION = (0, 3, 4)
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
