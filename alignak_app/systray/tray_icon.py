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

from PyQt5.Qt import QMenu, QSystemTrayIcon  # pylint: disable=no-name-in-module
from PyQt5.Qt import pyqtSignal  # pylint: disable=no-name-in-module

from alignak_app.core.utils import init_config
from alignak_app.dialogs.about_dialog import AboutQDialog
from alignak_app.systray.qactions_factory import QActionFactory
from alignak_app.threads.thread_manager import thread_manager

logger = getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    """
        Class who create QMenu and QAction.
    """

    update_tray = pyqtSignal(dict, name='tray_icon')

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        # Fields
        self.menu = QMenu(parent)
        self.qaction_factory = QActionFactory()
        self.app_about = None

    def build_menu(self, events_widget):
        """
        Initialize and create each action of menu.

        :param events_widget: events QWidget
        :type events_widget: alignak_app.dock.events_widget.EventsQListWidget
        """

        # Create actions
        self.create_dock_action()

        self.menu.addSeparator()

        self.create_reload_configuration(events_widget)
        self.create_about_action()

        self.menu.addSeparator()

        self.create_quit_action()

        self.setContextMenu(self.menu)

    def create_dock_action(self):
        """
        Create dashboard action

        """

        logger.info('Create Dashboard action')

        self.qaction_factory.create(
            'icon',
            _('Dock'),
            self
        )

        # Import dock from TrayIcon to fix application icon problem
        from alignak_app.dock.dock_widget import dock
        dock.initialize()
        dock.app_widget.show()
        self.qaction_factory.get_action('icon').triggered.connect(dock.app_widget.show)

        self.menu.addAction(self.qaction_factory.get_action('icon'))

    def create_reload_configuration(self, events_widget):
        """
        Create "reload" action

        :param events_widget: events QWidget
        :type events_widget: alignak_app.dock.events_widget.EventsQListWidget
        """

        self.qaction_factory.create(
            'refresh',
            _('Reload Configuration'),
            self
        )

        self.qaction_factory.get_action('refresh').triggered.connect(
            lambda: self.reload_configuration(events_widget)
        )

        self.menu.addAction(self.qaction_factory.get_action('refresh'))

        logger.info('Create Reload Action')

    def create_about_action(self):
        """
        Create AppAbout QWidget and "about" action.

        """

        self.app_about = AboutQDialog()
        self.app_about.create_window()

        self.qaction_factory.create(
            'about',
            _('About'),
            self
        )

        self.qaction_factory.get_action('about').triggered.connect(self.app_about.show_about)

        self.menu.addAction(self.qaction_factory.get_action('about'))

        logger.info('Create About Action')

    def create_quit_action(self):
        """
        Create quit action.

        """

        logger.info('Create Quit Action')

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

        thread_manager.stop()

        sys.exit(0)

    @staticmethod
    def reload_configuration(events_widget):
        """
        Reload configuration

        :param events_widget: events QWidget
        :type events_widget: alignak_app.dock.events_widget.EventsQListWidget
        """

        logger.info('Reload configuration...')
        init_config()
        events_widget.add_event('INFO', _('Configuration reloaded'))
