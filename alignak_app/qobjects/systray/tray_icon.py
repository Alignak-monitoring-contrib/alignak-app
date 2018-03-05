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
    Tray Icon
    +++++++++
    Tray Icon manage the creation of QSystemTrayIcon for Alignak-app menus
"""

import sys
from logging import getLogger

from PyQt5.Qt import QMenu, QSystemTrayIcon, QTimer

from alignak_app.utils.config import settings
from alignak_app.backend.backend import app_backend

from alignak_app.qobjects.app_main import AppQMainWindow
from alignak_app.qobjects.common.about import AboutQDialog
from alignak_app.qobjects.systray.qactions_factory import QActionFactory
from alignak_app.qobjects.dock.events import send_event

from alignak_app.qthreads.threadmanager import thread_manager


logger = getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    """
        Class who create QMenu and QAction.
    """

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        # Fields
        self.menu = QMenu(parent)
        self.qaction_factory = QActionFactory()
        self.app_about = None
        self.app_main = AppQMainWindow()
        self.connection_timer = QTimer()
        self.connection_nb = 3

    def build_menu(self):
        """
        Initialize and create each action of menu.

        """

        logger.info("Start TrayIcon...")

        self.connection_timer.setInterval(10000)
        self.connection_timer.start()
        self.connection_timer.timeout.connect(self.check_connection)

        # Create actions
        self.add_alignak_menu()
        self.menu.addSeparator()
        self.add_reload_menu()
        self.add_about_menu()
        self.menu.addSeparator()
        self.create_quit_action()

        self.setContextMenu(self.menu)

    def check_connection(self):
        """
        Check periodically connection for App

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

    def add_alignak_menu(self):
        """
        Create "dock" action

        """

        self.qaction_factory.create(
            'icon',
            _('Alignak-App'),
            self
        )

        self.app_main.initialize()
        self.qaction_factory.get_action('icon').triggered.connect(self.app_main.show)

        self.menu.addAction(self.qaction_factory.get_action('icon'))

    def add_reload_menu(self):
        """
        Create "reload" action

        """

        self.qaction_factory.create(
            'refresh',
            _('Reload Configuration'),
            self
        )

        self.qaction_factory.get_action('refresh').triggered.connect(self.reload_configuration)

        self.menu.addAction(self.qaction_factory.get_action('refresh'))

    def add_about_menu(self):
        """
        Create AppAbout QWidget and "about" action.

        """

        self.app_about = AboutQDialog()
        self.app_about.initialize()

        self.qaction_factory.create(
            'about',
            _('About'),
            self
        )

        self.qaction_factory.get_action('about').triggered.connect(self.app_about.show_about)

        self.menu.addAction(self.qaction_factory.get_action('about'))

    def create_quit_action(self):
        """
        Create quit action.

        """

        self.qaction_factory.create(
            'exit',
            'Quit',
            self
        )

        self.qaction_factory.get_action('exit').triggered.connect(self.quit_app)

        self.menu.addAction(self.qaction_factory.get_action('exit'))

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
