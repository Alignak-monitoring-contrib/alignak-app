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
from PyQt5.Qt import QApplication, QTimeEdit, QDateTimeEdit

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.common.actions import AckQDialog, DownQDialog, ActionsQWidget

settings.init_config()
init_localization()


class TestActionsQWidgets(unittest2.TestCase):
    """
        This file test actions QWidgets.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_acknowledge(self):
        """Initialize Acknowledge QDialog"""

        under_test = AckQDialog()
        under_test.initialize('host', 'my_host', 'Acknowledge requested by App')

        self.assertTrue(under_test.sticky)
        self.assertFalse(under_test.notify)

        self.assertEqual('Acknowledge requested by App', under_test.ack_comment_edit.toPlainText())

    def test_initialize_downtime(self):
        """Initialize Downtime QDialog"""

        under_test = DownQDialog()
        under_test.initialize('host', 'my_host', 'Downtime requested by App')

        self.assertTrue(under_test.fixed)
        self.assertTrue(under_test.duration)
        self.assertIsInstance(under_test.duration, QTimeEdit)
        self.assertEqual(under_test.duration_to_seconds(), 14400)
        self.assertTrue(under_test.start_time)
        self.assertIsInstance(under_test.start_time, QDateTimeEdit)
        self.assertTrue(under_test.end_time)
        self.assertIsInstance(under_test.end_time, QDateTimeEdit)
        self.assertEqual(
            under_test.end_time.dateTime().toTime_t() - under_test.start_time.dateTime().toTime_t(),
            7200
        )

        self.assertEqual('Downtime requested by App', under_test.comment_edit.toPlainText())

    def test_initialize_actions_widget(self):
        """Initialize Actions QWidget"""

        under_test = ActionsQWidget()

        self.assertIsNotNone(under_test.acknowledge_btn)
        self.assertIsNotNone(under_test.downtime_btn)
        self.assertIsNone(under_test.item)

        host_test = Host()
        under_test.initialize(host_test)

        self.assertIsNotNone(under_test.item)

    def test_actions_buttons_are_updated(self):
        """Actions Buttons are Updated"""

        under_test = ActionsQWidget()

        self.assertIsNone(under_test.item)

        host_test = Host()
        host_test.create(
            'id_1',
            {
                'ls_acknowledged': False,
                'ls_downtimed': False,
                '_id': 'id_1',
                'ls_state': 'DOWN'
            },
            'name'
        )
        under_test.initialize(host_test)

        # Actions buttons are True by default
        self.assertTrue(under_test.acknowledge_btn.isEnabled())
        self.assertTrue(under_test.downtime_btn.isEnabled())
        self.assertIsNotNone(under_test.item)

        # Log to backend and fill datamanager
        app_backend.login(
            settings.get_config('Alignak', 'username'),
            settings.get_config('Alignak', 'password')
        )
        data_manager.update_database('host', [host_test])

        # Update widget
        under_test.update_widget()
        webservice_test = settings.get_config('Alignak', 'webservice')
        self.assertTrue(webservice_test)

        if app_backend.ws_client.auth:
            # WS is set but not available, so buttons are disabled
            self.assertTrue(under_test.acknowledge_btn.isEnabled())
            self.assertTrue(under_test.downtime_btn.isEnabled())
        else:
            # WS is set but not available, so buttons are disabled
            self.assertFalse(under_test.acknowledge_btn.isEnabled())
            self.assertFalse(under_test.downtime_btn.isEnabled())

        # remove WS
        settings.set_config('Alignak', 'webservice', '')

        under_test.update_widget()

        # Only downtime button is Enabled, because host is UP
        self.assertTrue(under_test.acknowledge_btn.isEnabled())
        self.assertTrue(under_test.downtime_btn.isEnabled())

        # Restore configurations
        settings.set_config('Alignak', 'webservice', webservice_test)
        app_backend.connected = False
        app_backend.user = {}
