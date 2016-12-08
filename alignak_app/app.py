#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    App manage Alignak-App
"""

import sys
from logging import DEBUG, INFO

from alignak_app.core.logs import create_logger
from alignak_app.core.notifier import AppNotifier
from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import set_app_config, get_app_config
from alignak_app.systray.tray_icon import TrayIcon
from alignak_app.widgets.login import AppLogin
from alignak_app.core.backend import AppBackend

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QDialog  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
except ImportError:
    from PyQt4.QtGui import QIcon, QDialog  # pylint: disable=import-error

# Initialize logger
logger = create_logger()


class AlignakApp(object):
    """
        Class who build Alignak-app and initialize configuration, notifier and systray icon.
    """

    def __init__(self):
        self.tray_icon = None
        self.notifier = None

    def start(self):
        """
        The main function of Alignak-App

        """

        # Initialize configuration
        set_app_config()

        # Define level of logger
        if get_app_config('Alignak-App', 'debug', boolean=True):
            logger.setLevel(DEBUG)
            logger.info('Logger set to DEBUG')
        else:
            logger.setLevel(INFO)
            logger.info('Logger set to INFO')

        # If not backend url, stop application
        if get_app_config('Backend', 'backend_url'):
            # If not username and password, create login form,
            # else connect with config data.
            if not get_app_config('Backend', 'username') and \
                    not get_app_config('Backend', 'password'):
                login = AppLogin()
                login.create_widget()
                # If credentials are True, connect
                if login.exec_() == QDialog.Accepted:
                    self.run(login.app_backend)
                else:
                    logger.warning('Application close.')
                    exit()
            elif get_app_config('Backend', 'username') and \
                    not get_app_config('Backend', 'password'):
                self.run()
            elif get_app_config('Backend', 'username') and \
                    get_app_config('Backend', 'password'):
                self.run()
            else:
                logger.error('Please configure Alignak-app before starting it.')
                print('Please configure Alignak-app before starting it.')
                sys.exit()
        else:
            logger.error('Please configure Alignak-app before starting it.')
            print('Please configure Alignak-app before starting it.')
            sys.exit()

    def run(self, app_backend=None):  # pragma: no cover
        """
        Start all Alignak-app processes

        """

        if not app_backend:
            app_backend = AppBackend()
            app_backend.login()

        if 'token' not in app_backend.user:
            app_backend.user['token'] = app_backend.backend.token

        # Initialize notifier
        self.notifier = AppNotifier(self.get_icon(), app_backend)

        # Create QSystemTrayIcon
        self.tray_icon = TrayIcon(self.get_icon())
        self.tray_icon.build_menu(self.notifier.backend)
        self.tray_icon.show()

        self.notifier.start_process(self.tray_icon)

    @staticmethod
    def get_icon():
        """
        Set icon of application.

        """

        img = get_image_path('icon')
        icon = QIcon(img)

        return icon
