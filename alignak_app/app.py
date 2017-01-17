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
from time import sleep

from alignak_app.core.logs import create_logger
from alignak_app.core.notifier import AppNotifier
from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import init_config, get_app_config
from alignak_app.systray.tray_icon import TrayIcon
from alignak_app.widgets.login import AppLogin
from alignak_app.widgets.tick import tickManager, send_tick
from alignak_app.core.backend import AppBackend

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QDialog, QMessageBox  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QTimer  # pylint: disable=no-name-in-module
except ImportError:
    from PyQt4.QtGui import QDialog, QMessageBox  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer  # pylint: disable=import-error

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
        init_config()
        tickManager.start()

        # Define level of logger
        if get_app_config('Alignak-App', 'debug', boolean=True):
            logger.setLevel(DEBUG)
            logger.info('Logger set to DEBUG')
        else:
            logger.setLevel(INFO)
            logger.info('Logger set to INFO')

        # If not app_backend url, stop application
        if get_app_config('Backend', 'alignak_backend'):
            # If not username and password, create login form, else connect with config data.
            if not get_app_config('Backend', 'username') and \
                    not get_app_config('Backend', 'password'):
                login = AppLogin()
                login.create_widget()

                if login.exec_() == QDialog.Accepted:
                    self.run(login.app_backend)
                else:
                    logger.warning('Application close.')
                    exit(0)
            elif get_app_config('Backend', 'username') and \
                    not get_app_config('Backend', 'password'):
                self.run()
            elif get_app_config('Backend', 'username') and \
                    get_app_config('Backend', 'password'):
                self.run()
            else:
                logger.error('Please configure Alignak-app before starting it.')
                sys.exit()
        else:
            logger.error('Please configure Alignak-app before starting it.')
            sys.exit()

    @staticmethod
    def can_close():
        """
        Check if tick for bad identifier is send and close application.

        """

        if len(tickManager.ticks_to_send) == 0:
            QMessageBox.critical(None, 'Connection ERROR', 'Application will close !')
            sys.exit(0)

    @staticmethod
    def get_icon():
        """
        Set icon of application.

        """

        img = get_image_path('icon')
        icon = QIcon(img)

        return icon

    def run(self, app_backend=None):  # pragma: no cover
        """
        Start all Alignak-app processes

        """

        # If not login form
        if not app_backend:
            app_backend = AppBackend()
            connect = app_backend.login()
            if not connect:
                send_tick(
                    'ALERT',
                    'Your connection information are not accepted ! '
                    'Check your config file !'
                )
                timer = QTimer()
                timer.start(6000)
                timer.timeout.connect(self.can_close)
            else:
                send_tick('OK', 'Connected to Alignak Backend')

        if 'token' not in app_backend.user:
            app_backend.user['token'] = app_backend.backend.token

        # Initialize notifier
        self.notifier = AppNotifier(self.get_icon(), app_backend)

        # Create QSystemTrayIcon
        self.tray_icon = TrayIcon(self.get_icon())
        self.tray_icon.build_menu(self.notifier.backend)
        self.tray_icon.show()

        # If all is OK ;)
        start = bool(app_backend.get('livesynthesis'))
        if start:
            self.notifier.start(self.tray_icon)
