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

from alignak_app.core.backend import AppBackend
from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import init_config
from alignak_app.systray.tray_icon import TrayIcon
from alignak_app.dashboard.app_dashboard import Dashboard

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction


class TestTrayIcon(unittest2.TestCase):
    """
        This file test the TrayIcon class.
    """

    init_config()

    icon = QIcon(get_image_path('icon'))

    backend = AppBackend()
    backend.login()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_tray_icon(self):
        """Init TrayIcon and QMenu"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertIsInstance(under_test.menu, QMenu)

    def test_host_actions(self):
        """Hosts QActions are created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_hosts_actions()

        self.assertIsInstance(under_test.qaction_factory.get('hosts_up'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('hosts_down'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('hosts_unreachable'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('hosts_acknowledge'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('hosts_downtime'), QAction)

    def test_services_actions(self):
        """Services QActions are created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_services_actions()

        self.assertIsInstance(under_test.qaction_factory.get('services_ok'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('services_warning'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('services_critical'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('services_unknown'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('services_acknowledge'), QAction)
        self.assertIsInstance(under_test.qaction_factory.get('services_downtime'), QAction)

    def test_about_action(self):
        """About QAction is created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_about_action()

        self.assertIsNotNone(under_test.qaction_factory)
        self.assertIsInstance(under_test.qaction_factory.get('about'), QAction)

    def test_quit_action(self):
        """Quit QAction is created"""
        under_test = TrayIcon(TestTrayIcon.icon)

        self.assertFalse(under_test.qaction_factory.actions)

        under_test.create_quit_action()

        self.assertIsNotNone(under_test.qaction_factory.get('exit'))
        self.assertIsInstance(under_test.qaction_factory.get('exit'), QAction)

    def test_build_menu(self):
        """Build Menu add QActions"""
        under_test = TrayIcon(TestTrayIcon.icon)
        dashboard_test = Dashboard()

        # Assert no actions in Menu
        self.assertFalse(under_test.menu.actions())
        self.assertIsNone(under_test.app_about)
        self.assertIsNone(under_test.synthesis)
        self.assertIsNone(under_test.alignak_status)
        self.assertIsNotNone(under_test.qaction_factory)

        under_test.build_menu(self.backend, dashboard_test)

        # Assert actions are added in Menu
        self.assertTrue(under_test.menu.actions())
        self.assertIsNotNone(under_test.app_about)
        self.assertIsNotNone(under_test.synthesis)
        self.assertIsNotNone(under_test.alignak_status)
        self.assertIsNotNone(under_test.qaction_factory)

    def test_update_menus_actions(self):
        """Update Menu QActions"""
        under_test = TrayIcon(TestTrayIcon.icon)

        dashboard_test = Dashboard()
        under_test.build_menu(self.backend, dashboard_test)

        self.assertEqual('Hosts UP, Wait...',
                         under_test.qaction_factory.get('hosts_up').text())
        self.assertEqual('Hosts DOWN, Wait...',
                         under_test.qaction_factory.get('hosts_down').text())
        self.assertEqual('Hosts UNREACHABLE, Wait...',
                         under_test.qaction_factory.get('hosts_unreachable').text())

        self.assertEqual('Services OK, Wait...',
                         under_test.qaction_factory.get('services_ok').text())
        self.assertEqual('Services WARNING, Wait...',
                         under_test.qaction_factory.get('services_warning').text())
        self.assertEqual('Services CRITICAL, Wait...',
                         under_test.qaction_factory.get('services_critical').text())
        self.assertEqual('Services UNKNOWN, Wait...',
                         under_test.qaction_factory.get('services_unknown').text())

        synthesis = {
            'hosts': {
                'up': 1,
                'down': 2,
                'unreachable': 3,
                'acknowledge': 4,
                'downtime': 5,
            },
            'services': {
                'ok': 4,
                'warning': 5,
                'critical': 6,
                'unknown': 7,
                'unreachable': 8,
                'acknowledge': 9,
                'downtime': 10,

            }
        }

        under_test.update_menu_actions(synthesis)

        self.assertEqual('Hosts UP (1)',
                         under_test.qaction_factory.get('hosts_up').text())
        self.assertEqual('Hosts DOWN (2)',
                         under_test.qaction_factory.get('hosts_down').text())
        self.assertEqual('Hosts UNREACHABLE (3)',
                         under_test.qaction_factory.get('hosts_unreachable').text())
        self.assertEqual('Hosts ACKNOWLEDGE (4)',
                         under_test.qaction_factory.get('hosts_acknowledge').text())
        self.assertEqual('Hosts DOWNTIME (5)',
                         under_test.qaction_factory.get('hosts_downtime').text())

        self.assertEqual('Services OK (4)',
                         under_test.qaction_factory.get('services_ok').text())
        self.assertEqual('Services WARNING (5)',
                         under_test.qaction_factory.get('services_warning').text())
        self.assertEqual('Services CRITICAL (6)',
                         under_test.qaction_factory.get('services_critical').text())
        self.assertEqual('Services UNKNOWN (7)',
                         under_test.qaction_factory.get('services_unknown').text())
        self.assertEqual('Services UNREACHABLE (8)',
                         under_test.qaction_factory.get('services_unreachable').text())
        self.assertEqual('Services ACKNOWLEDGE (9)',
                         under_test.qaction_factory.get('services_acknowledge').text())
        self.assertEqual('Services DOWNTIME (10)',
                         under_test.qaction_factory.get('services_downtime').text())
