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

import sys

import unittest2
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu

from alignak_app.core.backend.client import BackendClient
from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.user import User
from alignak_app.core.utils.config import get_image
from alignak_app.core.utils.config import init_config
from alignak_app.locales.locales import init_localization
from alignak_app.pyqt.dock.widgets.events import init_event_widget
from alignak_app.pyqt.systray.tray_icon import TrayIcon


class TestTrayIcon(unittest2.TestCase):
    """
        This file test the TrayIcon class.
    """

    init_config()
    init_localization()

    icon = QIcon(get_image('icon'))

    backend = BackendClient()
    backend.login()

    data_manager.database['user'] = User()
    data_manager.database['user'].data = {}
    user_key = [
        '_realm', 'is_admin', 'back_role_super_admin', 'alias', 'name', 'notes', 'email',
        'can_submit_commands', 'token', 'host_notifications_enabled',
        'service_notifications_enabled', 'host_notification_period',
        'service_notification_period', 'host_notification_options',
        'service_notification_options',
    ]
    for key in user_key:
        if key == 'host_notifications_enabled' or key == 'service_notifications_enabled':
            data_manager.database['user'].data[key] = True
        else:
            data_manager.database['user'].data[key] = 'nothing'

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_tray_icon(self):
        """Init TrayIcon and QMenu"""
        init_event_widget()
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertIsInstance(under_test.menu, QMenu)

    def test_about_action(self):
        """About QAction is created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_about_action()

        self.assertIsNotNone(under_test.qaction_factory)
        self.assertIsInstance(under_test.qaction_factory.get_action('about'), QAction)

    def test_quit_action(self):
        """Quit QAction is created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_quit_action()

        self.assertIsNotNone(under_test.qaction_factory.get_action('exit'))
        self.assertIsInstance(under_test.qaction_factory.get_action('exit'), QAction)

    def test_build_menu(self):
        """Build Menu add QActions"""

        init_event_widget()
        data_manager.database['host'] = []
        data_manager.database['service'] = []

        for key in self.user_key:
            if key == 'host_notifications_enabled' or key == 'service_notifications_enabled':
                data_manager.database['user'].data[key] = True
            else:
                data_manager.database['user'].data[key] = 'nothing'

        under_test = TrayIcon(TestTrayIcon.icon)

        # Assert no actions in Menu
        self.assertFalse(under_test.menu.actions())
        self.assertIsNone(under_test.app_about)
        self.assertIsNotNone(under_test.qaction_factory)

        under_test.build_menu()

        # Assert actions are added in Menu
        self.assertTrue(under_test.menu.actions())
        self.assertIsNotNone(under_test.app_about)
        self.assertIsNotNone(under_test.qaction_factory)
