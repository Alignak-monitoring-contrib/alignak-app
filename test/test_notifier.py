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

from alignak_app.notifier import AppNotifier
from alignak_app.utils import get_alignak_home
from alignak_app.tray_icon import TrayIcon
from alignak_app.alignak_data import AlignakData
from alignak_app.popup import AppPopup

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


class TestAppNotifier(unittest2.TestCase):
    """
        This file test the AppNotifier class.
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

    def test_start_process(self):
        """Start Notifier Process"""
        under_test = AppNotifier(self.icon)

        self.assertIsNone(under_test.tray_icon)
        self.assertIsNone(under_test.config)
        self.assertIsNone(under_test.alignak_data)
        self.assertIsNone(under_test.popup)

        # Tray_icon for notifier
        tray_icon = TrayIcon(self.icon, self.config)
        tray_icon.build_menu()

        # Start process
        under_test.start_process(self.config, tray_icon)

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.config)
        self.assertIsNotNone(under_test.alignak_data)
        self.assertIsNotNone(under_test.popup)

    def test_check_data(self):
        """Check Data"""
        under_test = AppNotifier(self.icon)

        # Start notifier
        tray_icon = TrayIcon(self.icon, self.config)
        tray_icon.build_menu()
        under_test.start_process(self.config, tray_icon)

        # Check Actions are pending
        self.assertEqual('Hosts UP, Wait...',
                         under_test.tray_icon.hosts_actions['hosts_up'].text())
        self.assertEqual('Services OK, Wait...',
                         under_test.tray_icon.services_actions['services_ok'].text())

        # Check data...
        under_test.check_data()

        # ...so menu actions should be update
        self.assertNotEqual('Hosts UP, Wait...',
                         under_test.tray_icon.hosts_actions['hosts_up'].text())
        self.assertNotEqual('Services OK, Wait...',
                         under_test.tray_icon.services_actions['services_ok'].text())
