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
    App TrayIcon
    ++++++++++++
    App TrayIcon manage the creation of QSystemTrayIcon for Alignak-app menus
"""

import sys

from logging import getLogger

from PyQt5.Qt import QMenu, QSystemTrayIcon, QTimer, QAction, QIcon

from alignak_app.utils.config import settings, open_url
from alignak_app.backend.backend import app_backend

from alignak_app.qobjects.app_main import AppQMainWindow
from alignak_app.qobjects.about import AboutQDialog
from alignak_app.qobjects.events.events import send_event

from alignak_app.qobjects.threads.threadmanager import thread_manager


logger = getLogger(__name__)


class AppTrayIcon(QSystemTrayIcon):
    """
        Class who create `QMenu` and `QActions` for `QSystemTrayIcon` (displayed in task bar)
    """

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        # Fields
        self.menu = QMenu(parent)
        self.app_about = AboutQDialog()
        self.app_main = AppQMainWindow()
        self.connection_timer = QTimer()
        self.connection_nb = 3
        self.tray_actions = {
            'app': QAction(),
            'webui': QAction(),
            'reload': QAction(),
            'about': QAction(),
            'exit': QAction(),
        }

    def build_menu(self):
        """
        Initialize and create each QAction of QMenu

        """

        logger.info("Start TrayIcon...")

        self.connection_timer.setInterval(10000)
        self.connection_timer.start()
        self.connection_timer.timeout.connect(self.check_connection)

        # Create actions
        self.add_alignak_menu()
        self.add_webui_menu()
        self.menu.addSeparator()
        self.add_reload_menu()
        self.add_about_menu()
        self.menu.addSeparator()
        self.add_quit_menu()

        self.setContextMenu(self.menu)
        self.refresh_menus()

    def check_connection(self):
        """
        Check periodically connection to Alignak backend

        """

        if app_backend.connected:
            connect = app_backend.login(check=True)
            logger.info('App check connection: %s', app_backend.connection_status[connect])
            self.connection_nb = 3
        elif not app_backend.connected and self.connection_nb < 1:
            connect = app_backend.login(check=True)
            logger.warning('App check connection: %s', app_backend.connection_status[connect])
            self.connection_nb = 3
        elif not app_backend.connected:
            logger.warning('App check connection in %d0s', self.connection_nb)
            self.connection_nb -= 1
        else:
            pass

        self.app_main.dock.status_widget.update_status()
        self.refresh_menus()

    def add_alignak_menu(self):
        """
        Create and add to menu "app" QAction

        """

        self.app_main.initialize()

        self.tray_actions['app'].setIcon(QIcon(settings.get_image('icon')))
        self.tray_actions['app'].setText(_('Alignak-App'))
        self.tray_actions['app'].setToolTip(_('Display Alignak-App'))
        self.tray_actions['app'].triggered.connect(self.app_main.show)

        self.menu.addAction(self.tray_actions['app'])

    def add_webui_menu(self):
        """
        Create and add to menu "webui" QAction

        """

        self.tray_actions['webui'].setIcon(QIcon(settings.get_image('web')))
        self.tray_actions['webui'].setText(_('Go to WebUI'))
        self.tray_actions['webui'].setToolTip(_('Go to Alignak WebUI'))
        self.tray_actions['webui'].triggered.connect(
            lambda: open_url('livestate')
        )

        self.menu.addAction(self.tray_actions['webui'])

    def refresh_menus(self):
        """
        Refresh menu if needed

        """

        if settings.get_config('Alignak', 'webui'):
            self.tray_actions['webui'].setEnabled(True)
        else:
            self.tray_actions['webui'].setEnabled(False)

    def add_reload_menu(self):
        """
        Create and add to menu "reload" QAction

        """

        self.tray_actions['reload'].setIcon(QIcon(settings.get_image('refresh')))
        self.tray_actions['reload'].setText(_('Reload configuration'))
        self.tray_actions['reload'].setToolTip(_('Reload configuration'))
        self.tray_actions['reload'].triggered.connect(self.reload_configuration)

        self.menu.addAction(self.tray_actions['reload'])

    def add_about_menu(self):
        """
        Create and add to menu "about" QAction

        """

        self.app_about.initialize()

        self.tray_actions['about'].setIcon(QIcon(settings.get_image('about')))
        self.tray_actions['about'].setText(_('About...'))
        self.tray_actions['about'].setToolTip(_('About Alignak-app'))
        self.tray_actions['about'].triggered.connect(self.app_about.show_about)

        self.menu.addAction(self.tray_actions['about'])

    def add_quit_menu(self):
        """
        Create and add to menu "exit" QAction

        """

        self.tray_actions['exit'].setIcon(QIcon(settings.get_image('exit')))
        self.tray_actions['exit'].setText(_('Quit'))
        self.tray_actions['exit'].setToolTip(_('Quit Alignak-app'))
        self.tray_actions['exit'].triggered.connect(self.quit_app)

        self.menu.addAction(self.tray_actions['exit'])

    @staticmethod
    def quit_app():  # pragma: no cover
        """
        Quit application and close all widgets handle by application

        """

        thread_manager.stop_threads()
        logger.info('----- Alignak-App STOP -----')
        sys.exit(0)

    @staticmethod
    def reload_configuration():  # pragma: no cover
        """
        Reload configuration

        """

        logger.info('Reload configuration...')
        settings.init_config()
        settings.init_css()

        send_event('INFO', _('Configuration reloaded'), timer=True)
