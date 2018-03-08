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

import sys

import unittest2
from PyQt5.Qt import QApplication, QIcon, QMenu

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.user import User
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.events.events import init_event_widget
from alignak_app.qobjects.systray.tray_icon import AppTrayIcon


class TestTrayIcon(unittest2.TestCase):
    """
        This file test the AppTrayIcon class.
    """

    settings.init_config()
    init_localization()

    icon = QIcon(settings.get_image('icon'))

    data_manager.database['user'] = User()
    data_manager.database['user'].data = {}
    user_key = [
        '_realm', 'is_admin', 'back_role_super_admin', 'alias', 'name', 'notes', 'email',
        'can_submit_commands', 'token', 'host_notifications_enabled',
        'service_notifications_enabled', 'host_notification_period',
        'service_notification_period', 'host_notification_options',
        'service_notification_options',
    ]

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_tray_icon(self):
        """Init TrayIcon and QMenu"""

        under_test = AppTrayIcon(self.icon)

        self.assertIsInstance(under_test.menu, QMenu)

    def test_app_action(self):
        """Add App QAction"""

        # Init Event QWidget and fill DataManager for AppQMainWindow
        init_event_widget()
        data_manager.database['host'] = []
        data_manager.database['service'] = []
        for key in self.user_key:
            if key == 'host_notifications_enabled' or key == 'service_notifications_enabled':
                data_manager.database['user'].data[key] = True
            else:
                data_manager.database['user'].data[key] = 'nothing'

        under_test = AppTrayIcon(self.icon)

        self.assertFalse(under_test.tray_actions['app'].text())
        self.assertFalse(under_test.tray_actions['app'].toolTip())

        under_test.add_alignak_menu()

        self.assertTrue(under_test.tray_actions['app'].text())
        self.assertTrue(under_test.tray_actions['app'].toolTip())

    def test_reload_action(self):
        """Add Reload QAction"""

        under_test = AppTrayIcon(self.icon)

        self.assertFalse(under_test.tray_actions['reload'].text())
        self.assertFalse(under_test.tray_actions['reload'].toolTip())

        under_test.add_reload_menu()

        self.assertTrue(under_test.tray_actions['reload'].text())
        self.assertTrue(under_test.tray_actions['reload'].toolTip())

    def test_about_action(self):
        """Add About QAction"""

        under_test = AppTrayIcon(self.icon)

        self.assertFalse(under_test.tray_actions['about'].text())
        self.assertFalse(under_test.tray_actions['about'].toolTip())

        under_test.add_about_menu()

        self.assertTrue(under_test.tray_actions['about'].text())
        self.assertTrue(under_test.tray_actions['about'].toolTip())

    def test_quit_action(self):
        """Add Quit QAction"""

        under_test = AppTrayIcon(self.icon)

        self.assertFalse(under_test.tray_actions['exit'].text())
        self.assertFalse(under_test.tray_actions['exit'].toolTip())

        under_test.add_quit_menu()

        self.assertTrue(under_test.tray_actions['exit'].text())
        self.assertTrue(under_test.tray_actions['exit'].toolTip())

    def test_build_menu(self):
        """Build Menu add QActions"""

        # Init Event QWidget and fill DataManager for AppQMainWindow
        init_event_widget()
        data_manager.database['host'] = []
        data_manager.database['service'] = []
        for key in self.user_key:
            if key == 'host_notifications_enabled' or key == 'service_notifications_enabled':
                data_manager.database['user'].data[key] = True
            else:
                data_manager.database['user'].data[key] = 'nothing'

        under_test = AppTrayIcon(self.icon)

        # Assert no actions in Menu
        self.assertFalse(under_test.menu.actions())
        self.assertIsNotNone(under_test.app_about)
        self.assertIsNotNone(under_test.tray_actions)
        self.assertEqual(under_test.connection_nb, 3)

        under_test.build_menu()

        # Assert actions are added in Menu
        self.assertTrue(under_test.menu.actions())
        self.assertIsNotNone(under_test.app_about)
        self.assertIsNotNone(under_test.tray_actions)
        self.assertEqual(under_test.connection_nb, 3)

    def test_check_connection(self):
        """Tray Icon Check Connection"""

        under_test = AppTrayIcon(self.icon)
        from alignak_app.backend.backend import app_backend

        self.assertEqual(3, under_test.connection_nb)

        app_backend.connected = False

        # If App backend is not connected, "connection_nb" decrease
        under_test.check_connection()
        self.assertEqual(2, under_test.connection_nb)

        under_test.check_connection()
        self.assertEqual(1, under_test.connection_nb)

        under_test.check_connection()
        self.assertEqual(0, under_test.connection_nb)

        # If App still not connected, "connection_nb" is reset to 3
        under_test.check_connection()
        self.assertEqual(3, under_test.connection_nb)

        # If App backend back to connected, "connection_nb" is reset to 3
        under_test.connection_nb = 0
        app_backend.connected = True
        under_test.check_connection()
        self.assertEqual(3, under_test.connection_nb)

        # If App backend is connected, "connection_nb stay" at 3
        under_test.check_connection()
        self.assertEqual(3, under_test.connection_nb)

    def test_refresh_menus(self):
        """Refresh TrayIcon Menus"""

        under_test = AppTrayIcon(self.icon)

        # Webui is True
        self.assertTrue(under_test.tray_actions['webui'].isEnabled())

        old_webui = settings.get_config('Alignak', 'webui')
        settings.edit_setting_value('Alignak', 'webui', '')

        under_test.refresh_menus()

        # When refresh menu and WebUI is "False", QAction is not Enabled
        self.assertFalse(under_test.tray_actions['webui'].isEnabled())

        # Change settings does not update QAction
        settings.edit_setting_value('Alignak', 'webui', old_webui)
        self.assertFalse(under_test.tray_actions['webui'].isEnabled())

        under_test.refresh_menus()

        self.assertTrue(under_test.tray_actions['webui'].isEnabled())
