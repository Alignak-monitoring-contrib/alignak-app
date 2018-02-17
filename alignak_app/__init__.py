#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    This Python module is a desktop application, with a system tray icon, for Alignak solution.

    Application notify you when you have changes in your monitoring.
    You can trigger actions inside application, see status of monitored items, problems to solved
    and many other things.

    Alignak-app have the following architecture:

    * The `Client <api.html#module-alignak_app.core.backend>`_ manage requests with backend.
    * The `Thread Manager <api.html#module-alignak_app.pyqt.threads>`_ will launch request in
      client periodically.
    * The `Data Manager <api.html#module-alignak_app.core.backend>`_ will store data provided by
      client.
    * The `PyQt <api.html#module-alignak_app.pyqt>`_ display/update the data stored in data manager.

"""


# Application version and manifest
VERSION = (1, 1, 1)
__application__ = u"Alignak-App"
__libname__ = u"alignak_app"
__short_version__ = '.'.join((str(each) for each in VERSION[:2]))
__version__ = '.'.join((str(each) for each in VERSION[:4]))
__author__ = u"Estrada Matthieu"
__copyright__ = u"2015-2018 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__description__ = u"Desktop application, in system tray, for Alignak monitoring solution"
__releasenotes__ = u"Desktop application, in system tray, for Alignak monitoring solution"
__project_url__ = "https://github.com/Alignak-monitoring-contrib/alignak-app"
__doc_url__ = "http://alignak-app.readthedocs.io/en/develop/"
__alignak_url__ = "http://www.alignak.net/"

# Application Manifest
manifest = {
    'name': __application__,
    'version': __version__,
    'author': __author__,
    'description': __description__,
    'copyright': __copyright__,
    'license': __license__,
    'release': __releasenotes__,
    'url': __project_url__,
    'doc': __doc_url__
}
