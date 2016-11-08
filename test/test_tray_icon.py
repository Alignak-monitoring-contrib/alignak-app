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
except ImportError:
    from PyQt4.QtGui import QIcon
    from PyQt4.Qt import QApplication
    from PyQt4.Qt import QMenu


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
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertIsNotNone(under_test.config)
        self.assertIsInstance(under_test.menu, QMenu)

    def test_host_actions(self):
        under_test = TrayIcon(TestTrayIcon.icon, TestTrayIcon.config)

        self.assertFalse(under_test.hosts_actions)

        under_test.create_hosts_actions()

        self.assertTrue(under_test.hosts_actions)