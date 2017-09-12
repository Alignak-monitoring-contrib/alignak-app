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
from alignak_app.core.notifier import AppNotifier
from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import init_config
from alignak_app.systray.tray_icon import TrayIcon
from alignak_app.dashboard.app_dashboard import Dashboard

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


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

    def test_other_objects_do_not_modify_notifier(self):
        """Other objects do not Modify Notifier"""

        # TrayIcon and Dashboard for notifier
        tray_icon = TrayIcon(self.icon)
        dashboard = Dashboard()
        dashboard.initialize()

        under_test = AppNotifier()
        under_test.initialize(self.backend, tray_icon, dashboard)

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNotNone(under_test.dashboard)
        self.assertFalse(under_test.changes)

        tray_icon.build_menu(self.backend, dashboard)

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNotNone(under_test.dashboard)
        self.assertFalse(under_test.changes)

    def test_check_data(self):
        """Check Data modify TrayIcon Actions"""

        # TrayIcon and Dashboard for notifier
        tray_icon = TrayIcon(self.icon)
        dashboard = Dashboard()
        dashboard.initialize()

        under_test = AppNotifier()
        under_test.initialize(self.backend, tray_icon, dashboard)
        tray_icon.build_menu(self.backend, dashboard)

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

        # TrayIcon and Dashboard for notifier
        dashboard = Dashboard()
        dashboard.initialize()

        tray_icon = TrayIcon(self.icon)
        tray_icon.build_menu(self.backend, dashboard)

        # Initialize Notifier
        under_test = AppNotifier()
        under_test.initialize(self.backend, tray_icon, dashboard)

        # Changes are True, first_start is True
        self.assertFalse(under_test.changes)
        self.assertTrue(under_test.first_start)
        self.assertIsNone(under_test.old_synthesis)

    def test_diff_last_state(self):
        """Diff Last Backend SState"""

        self.backend = AppBackend()
        self.backend.login()

        # TrayIcon and Dashboard for notifier
        tray_icon_test = TrayIcon(self.icon)
        dashboard_test = Dashboard()

        notifier_test = AppNotifier()
        notifier_test.app_backend = self.backend
        notifier_test.tray_icon = tray_icon_test
        notifier_test.dashboard = dashboard_test

        # Notifier check data to get first synthesys counts
        notifier_test.check_data()

        # Get synthesis test to test diff between check
        synthesis = self.backend.synthesis_count()
        under_test = notifier_test.diff_last_states(synthesis)

        fields_test = {
            'hosts': {'up': 0, 'downtime': 0, 'down': 0, 'acknowledge': 0, 'unreachable': 0},
            'services': {
                'ok': 0,
                'acknowledge': 0,
                'unknown': 0,
                'critical': 0,
                'downtime': 0,
                'unreachable': 0,
                'warning': 0
            }
        }

        self.assertTrue(under_test)
        self.assertTrue('hosts' in under_test)
        self.assertTrue('services' in under_test)

        for state in fields_test['hosts']:
            self.assertTrue(state in under_test['hosts'])
            self.assertTrue(isinstance(under_test['hosts'][state], int))
        for state in fields_test['services']:
            self.assertTrue(state in under_test['services'])
            self.assertTrue(isinstance(under_test['services'][state], int))
