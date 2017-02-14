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

import copy
import sys

import unittest2

from alignak_app.core.backend import AppBackend
from alignak_app.core.notifier import AppNotifier
from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import init_config
from alignak_app.systray.tray_icon import TrayIcon

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

    def test_start_process(self):
        """Start Notifier Process"""

        # Tray_icon for notifier
        tray_icon = TrayIcon(self.icon)
        under_test = AppNotifier(self.backend, tray_icon)

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNotNone(under_test.dashboard)
        self.assertTrue(under_test.notify)

        tray_icon.build_menu(self.backend, under_test.dashboard)

        # Start notifier
        under_test.set_interval()

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNotNone(under_test.dashboard)
        self.assertTrue(under_test.notify)

    def test_check_data(self):
        """Check Data modify Actions"""

        tray_icon = TrayIcon(self.icon)
        under_test = AppNotifier(self.backend, tray_icon)
        tray_icon.build_menu(self.backend, under_test.dashboard)

        # Start notifier
        under_test.set_interval()

        # Check Actions are pending
        self.assertEqual('Hosts UP, Wait...',
                         under_test.tray_icon.qaction_factory.get('hosts_up').text())
        self.assertEqual('Services OK, Wait...',
                         under_test.tray_icon.qaction_factory.get('services_ok').text())

        # Check data...
        under_test.check_data()

        # ...so menu actions should be update
        self.assertNotEqual('Hosts UP, Wait...',
                            under_test.tray_icon.qaction_factory.get('hosts_up').text())
        self.assertNotEqual('Services OK, Wait...',
                            under_test.tray_icon.qaction_factory.get('services_ok').text())

    def test_states_change(self):
        """States and Notify Changes"""
        self.backend = AppBackend()
        self.backend.login()

        tray_icon = TrayIcon(self.icon)
        under_test = AppNotifier(self.backend, tray_icon)

        # Start notifier
        tray_icon.build_menu(self.backend, under_test.dashboard)
        under_test.set_interval()

        # "start_process" set notify to True
        self.assertTrue(under_test.notify)

        # "get_all_state" to fill states
        # 1 - First time, states are fill
        self.assertFalse(under_test.app_backend.states)
        under_test.app_backend.synthesis_count()
        # 2 - Next time, states will be filled
        self.assertTrue(under_test.app_backend.states)

        # Copy state
        old_states = copy.deepcopy(under_test.app_backend.states)
        under_test.diff_since_last_check(old_states)

        # "check_changes" set notify to False if no changes
        self.assertFalse(under_test.notify)

        # Modify "states" to set notify to True
        under_test.app_backend.states['hosts']['up'] += 1
        under_test.diff_since_last_check(old_states)

        self.assertTrue(under_test.notify)
