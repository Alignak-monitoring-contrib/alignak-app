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
    App
    ~~~
    App manages the creation of QObjects for the whole application:

    * Creation of QObject for App Main (QMainWindow)
    * Creation of QProgressbar until the Data Manager is ready
"""

import os
import sys
import time

from logging import DEBUG, INFO

from PyQt5.Qt import QDialog, QMessageBox, QTimer, QProgressBar, Qt, pyqtSignal, QObject, QIcon
from PyQt5.Qt import QWidget, QVBoxLayout, QLabel

from alignak_app import __application__, __version__
from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.utils.logs import create_logger

from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.events import init_event_widget
from alignak_app.qobjects.common.widgets import center_widget
from alignak_app.qobjects.login.login import LoginQDialog
from alignak_app.qobjects.systray.tray_icon import TrayIcon

from alignak_app.qthreads.threadmanager import thread_manager

# Init App settings before importing QWidgets
settings.init_config()
settings.init_css()
init_localization()
logger = create_logger()


class AppProgressQWidget(QWidget):
    """
        Class who create a small widget for App start progression
    """

    def __init__(self, parent=None):
        super(AppProgressQWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(250, 80)
        self.setStyleSheet(settings.css_style)
        self.progress_bar = AppProgressBar()

    def initialize(self):
        """
        Initialize the QWidget

        """

        title_lbl = QLabel('%s - %s' % (__application__, __version__))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setObjectName('start')
        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)
        layout.addWidget(self.progress_bar)


class AppProgressBar(QProgressBar):
    """
        AppProgressBar in busy mode with text displayed at the center.
    """

    def __init__(self):
        super(AppProgressBar, self).__init__()
        self.setRange(0, 0)
        self.setAlignment(Qt.AlignCenter)
        self._text = None

    def set_text(self, text):
        """
        Set text of QProgressBar

        :param text: text of progress bar
        :type text: str
        """

        self._text = text

    def text(self):
        """
        Overload: text(self) -> str

        :return: text of progress bar
        :rtype: str
        """

        return self._text


class AlignakApp(QObject):
    """
        Class who build Alignak-app and initialize configurations and systray icon.
    """

    reconnecting = pyqtSignal(str, name='reconnecting')

    def __init__(self, parent=None):
        super(AlignakApp, self).__init__(parent)
        self.tray_icon = None
        self.reconnect_mode = False

    def start(self):  # pragma: no cover
        """
        The main function of Alignak-App

        """

        # Define level of logger and log main informations
        logger.name = 'alignak_app'
        if settings.get_config('Log', 'debug', boolean=True):
            logger.setLevel(DEBUG)
            logger.info('- [Log Level]: DEBUG')
        else:
            logger.setLevel(INFO)
            logger.info('- [Log Level]: INFO')

        logger.info('- [ALIGNAKAPP_LOG_DIR]: %s', os.environ['ALIGNAKAPP_LOG_DIR'])
        logger.info('- [ALIGNAKAPP_USER_CFG]: %s', os.environ['ALIGNAKAPP_USER_CFG'])
        logger.info('- [ALIGNAKAPP_APP_CFG]: %s', os.environ['ALIGNAKAPP_APP_CFG'])
        logger.info('- [%s]: %s',
                    os.path.split(settings.settings['settings'])[1], settings.settings['settings'])
        logger.info('- [%s]: %s',
                    os.path.split(settings.settings['images'])[1], settings.settings['images'])

        self.reconnecting.connect(self.app_reconnecting_mode)
        self.run(app_backend.login())

    def app_reconnecting_mode(self, error):  # pragma: no cover
        """
        Set AlignakApp in reconnect mode and try to login to Backend

        :param error: string error to display in banner
        :type error: str
        """

        self.reconnect_mode = True
        timer = QTimer(self)

        logger.error('Connection Error: %s', error)

        # Stop thread_name manager
        logger.warning('Application reconnecting MODE: %s', self.reconnect_mode)
        thread_manager.stop_threads()

        def connect_to_backend():
            """Try to log in to Backend"""
            try:
                connect = app_backend.login()
                assert connect
                timer.stop()
                # If connect, reconnecting is disable and threads restart
                self.reconnect_mode = False
                thread_manager.start()
                logger.info('Connection restored : %s', connect)
            except AssertionError:
                logger.error('Backend is still unreachable...')

        if timer.isActive():
            pass
        else:
            timer.start(5000)
            timer.timeout.connect(connect_to_backend)

    def run(self, connected):  # pragma: no cover
        """
        Start all Alignak-app processes and create AppBackend if connection by config file.

        """

        # Check if connected
        if connected:
            # Start ThreadManager
            for _ in range(0, 5):
                thread_manager.launch_threads()

            # Give AlignakApp for AppBackend reconnecting mode
            app_backend.app = self

            if 'token' not in app_backend.user:
                app_backend.user['token'] = app_backend.backend.token

            # Create Progress Bar
            app_progress = AppProgressQWidget()
            app_progress.initialize()
            center_widget(app_progress)

            logger.info("Preparing DataManager...")
            while data_manager.is_ready() != 'READY':
                app_progress.show()
                for _ in range(0, 100):
                    t = time.time()
                    while time.time() < t + 0.01:
                        status = data_manager.is_ready()
                        app_progress.progress_bar.set_text('%s' % status)
                        self.parent().processEvents()
            app_progress.close()

            # Launch other threads and run TrayIcon()
            logger.info("Datamanager is ready :)")
            thread_manager.start()
            init_event_widget()
            self.tray_icon = TrayIcon(QIcon(settings.get_image('icon')))
            self.tray_icon.build_menu()
            self.tray_icon.show()

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
