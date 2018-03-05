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

    * The :class:`BackendClient <alignak_app.backend.backend.BackendClient>` manage requests with
      Alignak backend.
    * The :class:`ThreadManager <alignak_app.qthreads.threadmanager.ThreadManager>` will
      launch :class:`BackendQThread(s) <alignak_app.qthreads.thread.BackendQThread>` to
      trigger requests in :class:`BackendClient <alignak_app.backend.backend.BackendClient>`.
    * The :class:`DataManager <alignak_app.backend.datamanager.DataManager>` will store data
      provided by :class:`BackendClient <alignak_app.backend.backend.BackendClient>` in
      :class:`Items <alignak_app.items>`.
    * The :class:`QObjects <alignak_app.qobjects>` package display/update the data stored in
      :class:`DataManager <alignak_app.backend.datamanager.DataManager>`.
    * The :class:`Utils <alignak_app.utils>` package contains settings, logs, installation,...
    * The :class:`Locales <alignak_app.locales>` package contains translations.

    Alignak-app will use a system of :class:`Installer <alignak_app.utils.installer.Installer>`
    who use **environment variables** to run:

    * ``ALIGNAKAPP_USR_DIR``: contains settings of user (**write rights**)
    * ``ALIGNAKAPP_LOG_DIR``: contains log files of App (**write rights**)
    * ``ALIGNAKAPP_APP_DIR``: contains binaries of App (images, css, languages) (**read rights**)

    The :class:`Login <alignak_app.qobjects.login.login.LoginQDialog>` manage user login if needed.

"""


# Application version and manifest
VERSION = (1, 3, 0)
__application__ = u"Alignak-App"
__libname__ = u"alignak_app"
__short_version__ = '.'.join((str(each) for each in VERSION[:2]))
__version__ = '.'.join((str(each) for each in VERSION[:4]))
__author__ = u"Estrada Matthieu"
__copyright__ = u"2015-2018 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__description__ = u"Desktop application, with system tray, for Alignak monitoring solution"
__releasenotes__ = u"Desktop application, with system tray, for Alignak monitoring solution"
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
