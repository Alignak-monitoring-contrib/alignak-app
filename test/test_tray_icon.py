#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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

import unittest2
import configparser
import sys
import os

from alignak_app.tray_icon import TrayIcon
from alignak_app.utils import get_alignak_home

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QMenu
    from PyQt5.QtWidgets import QAction
except ImportError:
    from PyQt4.QtGui import QIcon
    from PyQt4.Qt import QApplication
    from PyQt4.Qt import QMenu
    from PyQt4.Qt import QAction


class TestTrayIcon(unittest2.TestCase):
    """
        This file test the TrayIcon class.
    """

    config_file = get_alignak_home() + '/alignak_app/settings.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)

    qicon_path = get_alignak_home() \
                 + config.get('Config', 'path') \
                 + config.get('Config', 'img') \
                 + '/'
    img = os.path.abspath(qicon_path + config.get('Config', 'icon'))
    icon = QIcon(img)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_tray_icon(self):
        """Init TrayIcon"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertIsNotNone(under_test.config)
        self.assertIsInstance(under_test.menu, QMenu)

    def test_host_actions(self):
        """Hosts Actions"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertFalse(under_test.hosts_actions)

        under_test.create_hosts_actions()

        self.assertTrue(under_test.hosts_actions)
        self.assertIsInstance(under_test.hosts_actions['hosts_up'], QAction)
        self.assertIsInstance(under_test.hosts_actions['hosts_down'], QAction)
        self.assertIsInstance(under_test.hosts_actions['hosts_unreach'], QAction)

    def test_services_actions(self):
        """Services Actions"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertFalse(under_test.services_actions)

        under_test.create_services_actions()

        self.assertTrue(under_test.services_actions)
        self.assertIsInstance(under_test.services_actions['services_ok'], QAction)
        self.assertIsInstance(under_test.services_actions['services_warning'], QAction)
        self.assertIsInstance(under_test.services_actions['services_critical'], QAction)
        self.assertIsInstance(under_test.services_actions['services_unknown'], QAction)

    def test_about_action(self):
        """About Action"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertIsNone(under_test.about_menu)

        under_test.create_about_action()

        self.assertIsNotNone(under_test.about_menu)
        self.assertIsInstance(under_test.about_menu, QAction)

    def test_quit_action(self):
        """Quit Action"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertIsNone(under_test.quit_menu)

        under_test.create_quit_action()

        self.assertIsNotNone(under_test.quit_menu)
        self.assertIsInstance(under_test.quit_menu, QAction)

    def test_build_menu(self):
        """Menu have actions"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        # Assert no actions in Menu
        self.assertFalse(under_test.menu.actions())

        under_test.build_menu()

        # Assert actions are added in Menu
        self.assertTrue(under_test.menu.actions())

    def test_update_menus_actions(self):
        """Update Menu Actions"""
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        under_test.build_menu()

        self.assertEqual('Hosts UP, Wait...',
                         under_test.hosts_actions['hosts_up'].text())
        self.assertEqual('Hosts DOWN, Wait...',
                         under_test.hosts_actions['hosts_down'].text())
        self.assertEqual('Hosts UNREACHABLE, Wait...',
                         under_test.hosts_actions['hosts_unreach'].text())

        self.assertEqual('Services OK, Wait...',
                         under_test.services_actions['services_ok'].text())
        self.assertEqual('Services WARNING, Wait...',
                         under_test.services_actions['services_warning'].text())
        self.assertEqual('Services CRITICAL, Wait...',
                         under_test.services_actions['services_critical'].text())
        self.assertEqual('Services UNKNOWN, Wait...',
                         under_test.services_actions['services_unknown'].text())

        hosts_states = dict(
            up=1,
            down=2,
            unreachable=3
        )
        services_states = dict(
            ok=4,
            warning=5,
            critical=6,
            unknown=7
        )

        under_test.update_menu_actions(hosts_states, services_states)

        self.assertEqual('Hosts UP (1)',
                         under_test.hosts_actions['hosts_up'].text())
        self.assertEqual('Hosts DOWN (2)',
                         under_test.hosts_actions['hosts_down'].text())
        self.assertEqual('Hosts UNREACHABLE (3)',
                         under_test.hosts_actions['hosts_unreach'].text())

        self.assertEqual('Services OK (4)',
                         under_test.services_actions['services_ok'].text())
        self.assertEqual('Services WARNING (5)',
                         under_test.services_actions['services_warning'].text())
        self.assertEqual('Services CRITICAL (6)',
                         under_test.services_actions['services_critical'].text())
        self.assertEqual('Services UNKNOWN (7)',
                         under_test.services_actions['services_unknown'].text())
