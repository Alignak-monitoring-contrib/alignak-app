#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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
import time

from logging import DEBUG, INFO

from alignak_app.core.logs import create_logger
from alignak_app.threads.thread_manager import thread_manager
from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_image_path, get_main_folder, get_app_workdir
from alignak_app.core.utils import init_config, get_app_config
from alignak_app.core.locales import init_localization
from alignak_app.widgets.login import AppLogin
from alignak_app.core.backend import app_backend
from alignak_app.systray.tray_icon import TrayIcon

from PyQt5.QtWidgets import QDialog, QMessageBox, QSplashScreen  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QTimer, QProgressBar, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import pyqtSignal, QObject, QIcon  # pylint: disable=no-name-in-module

# Initialize app config, logger and localization
init_config()
logger = create_logger()
init_localization()


class AlignakApp(QObject):
    """
        Class who build Alignak-app and initialize configuration, notifier and systray icon.
    """

    reconnecting = pyqtSignal(str, name='reconnecting')

    def __init__(self, parent=None):
        super(AlignakApp, self).__init__(parent)
        self.tray_icon = None
        self.reconnect_mode = False

    def start(self):
        """
        The main function of Alignak-App

        """

        # Define level of logger
        logger.name = 'alignak_app.app'
        if get_app_config('Log', 'debug', boolean=True):
            logger.setLevel(DEBUG)
            logger.info('Logger Level is: DEBUG')
        else:
            logger.setLevel(INFO)
            logger.info('Logger Level is: INFO')

        logger.info('App WorkDir = %s', get_app_workdir())
        logger.info('App MainDir = %s', get_main_folder())

        # If not app_backend url, stop application
        if get_app_config('Alignak', 'backend'):
            # If not username and password, create login form, else connect with config data.
            if not get_app_config('Alignak', 'username') and \
                    not get_app_config('Alignak', 'password'):  # pragma: no cover - Not testable
                login = AppLogin()
                login.create_widget()

                if login.exec_() == QDialog.Accepted:
                    username = str(login.username_line.text())
                    password = str(login.password_line.text())
                    self.run(username, password)
                else:
                    logger.info('Alignak-App closes...')
                    sys.exit(0)
            elif get_app_config('Alignak', 'username') and \
                    not get_app_config('Alignak', 'password'):
                self.run()
            elif get_app_config('Alignak', 'username') and \
                    get_app_config('Alignak', 'password'):
                self.run()
            else:
                self.display_error_msg()

        else:
            self.display_error_msg()

    def reconnect_to_backend(self, error):  # pragma: no cover
        """
        Set AlignakApp in reconnect mode and try to login to Backend

        :param error: string error to display in banner
        :type error: str
        """

        self.reconnect_mode = True
        logger.warning('Application reconnecting MODE: %s', self.reconnecting)
        logger.error('... caused by %s', error)
        timer = QTimer(self)

        def connect_to_backend():
            """Try to log in to Backend"""
            try:
                connect = app_backend.login()
                assert connect
                # If connect, reconnecting is disable
                timer.stop()
                logger.info('Connection restored : %s', connect)
                self.reconnect_mode = False
            except AssertionError:
                logger.error('Backend is still unreachable...')

        if timer.isActive():
            pass
        else:
            timer.start(10000)
            timer.timeout.connect(connect_to_backend)

    def run(self, username=None, password=None):  # pragma: no cover
        """
        Start all Alignak-app processes and create AppBackend if connection by config file.

        """

        if username and password:
            app_backend.login(username, password)
        else:
            app_backend.login()

        # Check if connected
        if app_backend.connected:
            # Start ThreadManager
            thread_manager.start()

            # Give AlignakApp for AppBackend reconnecting mode
            app_backend.app = self

            if 'token' not in app_backend.user:
                app_backend.user['token'] = app_backend.backend.token

            splash_icon = QPixmap(get_image_path('alignak'))
            splash = QSplashScreen(splash_icon)

            progressbar = QProgressBar(splash)
            progressbar.setTextVisible(False)
            progressbar.setStyleSheet('border-top: none; color: none;')
            progressbar.setFixedSize(splash_icon.width(), splash_icon.height())
            progressbar.setAlignment(Qt.AlignCenter)

            splash.setMask(splash_icon.mask())
            splash.show()

            logger.info("Preparing DataManager...")
            while not data_manager.is_ready():
                for i in range(0, 100):
                    progressbar.setValue(i)
                    t = time.time()
                    while time.time() < t + 0.01:
                        self.parent().processEvents()

            logger.info("Starting Dock...")

            # Prevent from: QWidget: Must construct a QApplication before a QWidget
            from alignak_app.dock.dock_widget import dock
            from alignak_app.dock.events_widget import events_widget

            splash.finish(dock)
            dock.initialize()

            logger.info("Start TrayIcon...")
            self.tray_icon = TrayIcon(QIcon(get_image_path('icon')))
            self.tray_icon.build_menu(dock)
            self.tray_icon.show()

            # Send Welcome Banner
            events_widget.add_event(
                'OK',
                _('Welcome %s, you are connected to Alignak Backend') %
                data_manager.database['user'].name,
            )

            dock.app_widget.show()
        else:
            # In case of data provided in config file fails
            logger.error(
                'Fails to connect with the information provided in the configuration file !'
            )
            login = AppLogin()
            login.create_widget()

            if login.exec_() == QDialog.Accepted:
                username = str(login.username_line.text())
                password = str(login.password_line.text())
                self.run(username, password)
            else:
                logger.info('Alignak-App closes...')
                sys.exit(0)

    @staticmethod
    def display_error_msg():  # pragma: no cover
        """
        Display a QMessageBox error in case app fail to start

        """

        logger.error('Something seems wrong in your configuration.'
                     'Please configure Alignak-app before starting it. '
                     'And make sure the backend is available')

        QMessageBox.critical(
            None,
            _('Configuration / Connection ERROR'),
            _(
                'Something seems wrong in your configuration. '
                'Please configure Alignak-app before starting it. '
                'And make sure the backend is available'
            )
        )
        sys.exit()
