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
    Tray_icon manage the creation of Application menus.
"""

import sys
from logging import getLogger

from PyQt5.Qt import QMenu, QSystemTrayIcon

from alignak_app.core.utils.config import init_config, init_css

from alignak_app.pyqt.systray.dialogs.about import AboutQDialog
from alignak_app.pyqt.systray.qactions_factory import QActionFactory
from alignak_app.pyqt.threads.thread_manager import thread_manager
from alignak_app.pyqt.dock.widgets.dock import DockQWidget
from alignak_app.pyqt.dock.widgets.events import send_event


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
        self.dock = DockQWidget()

    def build_menu(self):
        """
        Initialize and create each action of menu.

        """

        logger.info("Start TrayIcon...")
        # Create actions
        self.create_dock_action()

        self.menu.addSeparator()

        self.create_reload_configuration()
        self.create_about_action()

        self.menu.addSeparator()

        self.create_quit_action()

        self.setContextMenu(self.menu)

    def create_dock_action(self):
        """
        Create "dock" action

        """

        logger.debug('Create Dock Action')

        self.qaction_factory.create(
            'icon',
            _('Dock'),
            self
        )

        self.dock.initialize()
        self.dock.show_dock()
        self.qaction_factory.get_action('icon').triggered.connect(self.dock.show_dock)

        self.menu.addAction(self.qaction_factory.get_action('icon'))

    def create_reload_configuration(self):
        """
        Create "reload" action

        """

        logger.debug('Create Reload Action')

        self.qaction_factory.create(
            'refresh',
            _('Reload Configuration'),
            self
        )

        self.qaction_factory.get_action('refresh').triggered.connect(self.reload_configuration)

        self.menu.addAction(self.qaction_factory.get_action('refresh'))

    def create_about_action(self):
        """
        Create AppAbout QWidget and "about" action.

        """

        logger.debug('Create About Action')

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

        logger.debug('Create Quit Action')

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

        sys.exit(0)

    @staticmethod
    def reload_configuration():
        """
        Reload configuration

        """

        logger.info('Reload configuration...')
        init_config()
        init_css()

        send_event('INFO', _('Configuration reloaded'), timer=True)
