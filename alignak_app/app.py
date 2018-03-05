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
    App manages the creation of all objects and QObjects for the whole application:

    * Creation of :class:`AppProgressBar <alignak_app.app.AppProgressBar>` until the Data Manager is
      ready
    * Creation of :class:`AppQMainWindow <alignak_app.qobjects.app_main.AppQMainWindow>`
    * Creation of standard python objects (settings, css, localization)
"""

import os
import sys
import time

from logging import DEBUG, INFO
from PyQt5.Qt import QApplication, QObject, QIcon, Qt, QProgressBar, QWidget, QLabel, QVBoxLayout
from PyQt5.Qt import QTimer

from alignak_app import __application__, __version__

from alignak_app.utils.config import settings
from alignak_app.utils.logs import create_logger
from alignak_app.locales.locales import init_localization

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager

from alignak_app.qthreads.threadmanager import thread_manager, BackendQThread
from alignak_app.qobjects.common.widgets import center_widget
from alignak_app.qobjects.login.login import LoginQDialog
from alignak_app.qobjects.dock.events import init_event_widget
from alignak_app.qobjects.systray.tray_icon import TrayIcon

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
        # Fields
        self.progress_bar = AppProgressBar()

    def initialize(self):
        """
        Initialize the QWidget

        """

        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        title_lbl = QLabel('%s - %s' % (__application__, __version__))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setObjectName('start')
        title_lbl.setFixedHeight(30)
        layout.addWidget(title_lbl)

        self.progress_bar.setFixedHeight(30)
        layout.addWidget(self.progress_bar)

        layout.setAlignment(Qt.AlignCenter)


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


class AlignakApp(QObject):  # pragma: no cover
    """
        Class who build Alignak-app QObjects, initialize configurations, systray icon
        and Thread Manager.
    """

    def __init__(self):
        super(AlignakApp, self).__init__()
        self.tray_icon = None
        self.threadmanager_timer = QTimer()

    def start(self, username=None, password=None):
        """
        Start Alignak-app

        """

        # Logger
        logger.name = 'alignak_app.app'
        if settings.get_config('Log', 'debug', boolean=True):
            logger.setLevel(DEBUG)
        else:
            logger.setLevel(INFO)

        logger.info('\n')
        logger.info('----- Alignak-App START -----')
        logger.info('- Running Version : "%s"', __version__)
        logger.info('- Alignak-App Env :')
        logger.info('[ALIGNAKAPP_APP_DIR] = %s', os.environ['ALIGNAKAPP_APP_DIR'])
        logger.info('[ALIGNAKAPP_USR_DIR] = %s', os.environ['ALIGNAKAPP_USR_DIR'])
        logger.info('[ALIGNAKAPP_LOG_DIR] = %s', os.environ['ALIGNAKAPP_LOG_DIR'])
        logger.info('- Config File     : %s', settings.settings['settings'])
        logger.info('- Debug Activate  : %s', settings.get_config('Log', 'debug', boolean=True))
        logger.info('- Alignak Backend : %s', settings.get_config('Alignak', 'backend'))

        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        # Connection to Backend
        if settings.get_config('Alignak', 'username') and not username and not password:
            username = settings.get_config('Alignak', 'username')
            password = settings.get_config('Alignak', 'password')

        if not app_backend.login(username, password):
            login = LoginQDialog()
            login.create_widget()

            while not app_backend.connected:
                login.exec_()

        # Launch start threads
        thread_to_launch = thread_manager.get_threads_to_launch()
        thread_to_launch.remove('history')
        thread_to_launch.remove('notifications')
        logger.info("Filling the local database: %s", thread_to_launch)

        launched_threads = []
        for thread in thread_to_launch:
            backend_thread = BackendQThread(thread)
            backend_thread.start()

            launched_threads.append(backend_thread)

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
                    app.processEvents()

        app_progress.close()

        init_event_widget()
        requests_interval = int(settings.get_config('Alignak-app', 'requests_interval')) * 1000
        self.threadmanager_timer.setInterval(requests_interval)
        self.threadmanager_timer.start()
        self.threadmanager_timer.timeout.connect(self.check_threads)

        self.tray_icon = TrayIcon(QIcon(settings.get_image('icon')))
        self.tray_icon.build_menu()
        self.tray_icon.show()

        while self.quit_launched_threads(launched_threads):
            pass

        sys.exit(app.exec_())

    @staticmethod
    def quit_launched_threads(launched_threads):
        """
        Exit the threads that were started when the application started

        :param launched_threads: list of threads that have been launched
        :type launched_threads: list
        :return: empty list if all the threads have been left or current list
        :rtype: list
        """

        for old_thread in launched_threads:
            if old_thread.isFinished():
                old_thread.quit()
                old_thread.wait()
                launched_threads.remove(old_thread)

        return launched_threads

    @staticmethod
    def check_threads():
        """
        Launch periodically threads

        """

        # Cleaning threads who are finished
        thread_manager.clean_threads()

        # Launch or stop threads
        if app_backend.connected:
            thread_manager.launch_threads()
        else:
            logger.debug(
                'Can\'t launch Request threads, App is not connected to backend [%s] !',
                settings.get_config('Alignak', 'backend')
            )
            thread_manager.stop_threads()
