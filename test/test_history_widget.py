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
from PyQt5.Qt import QApplication, QWidget, QLabel, QSize

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.history import History
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.host.history import HistoryQWidget, AppQFrame

settings.init_config()
init_localization()


class TestHistoryQWidget(unittest2.TestCase):
    """
        This file test the HistoryQWidget class.
    """

    history_data_test = [
        {
            '_updated': 'Tue, 19 Sep 2017 13:07:16 GMT',
            'service_name': 'Load',
            'type': 'ack.processed',
            'message': 'Service Load acknowledged by admin, from Alignak-app',
        },
        {
            '_updated': 'Tue, 19 Sep 2017 13:07:01 GMT',
            'service_name': 'Load',
            'type': 'downtime.add',
            'message': 'Service Load acknowledged by admin, from Alignak-app',
        },
        {
            '_updated': 'Tue, 19 Sep 2017 13:05:26 GMT',
            'service_name': '',
            'type': 'check.result',
            'message': 'UNREACHABLE[HARD] (False/False): ERROR: netsnmp : No response from ...',
        },
        {
            '_updated': 'Tue, 19 Sep 2017 13:05:26 GMT',
            'service_name': 'NetworkUsage',
            'type': 'check.result',
            'message': 'UNREACHABLE[HARD] (False/False): ERROR: Description table : ...',
        }
    ]
    history_test = History()
    history_test.create('id', history_data_test, 'hostname')

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize History QWidget"""

        under_test = HistoryQWidget()

        self.assertIsNone(under_test.layout())
        self.assertIsInstance(under_test.app_widget, AppQFrame)
        self.assertIsNotNone(under_test.table_headers)
        self.assertIsNotNone(under_test.history_title)

        data_manager.database['history'].append(self.history_test)
        under_test.initialize()

        self.assertIsNotNone(under_test.layout())
        self.assertEqual(under_test.app_widget.windowTitle(), "History")
        self.assertIsInstance(under_test.app_widget, AppQFrame)
        self.assertIsNotNone(under_test.table_headers)
        self.assertIsNotNone(under_test.history_title)

    def test_update_history_data(self):
        """Update History QTableWidget Data"""

        under_test = HistoryQWidget()
        under_test.initialize()

        for i in range(0, len(self.history_test.data)):
            self.assertIsNone(under_test.history_table.cellWidget(i, 0))

        under_test.update_history_data('hostname', self.history_test)

        for i in range(0, len(self.history_test.data)):
            self.assertIsNotNone(under_test.history_table.cellWidget(i, 0))

    def test_get_event_widget(self):
        """Get Event History QWidget"""

        under_test = HistoryQWidget()

        event_test = self.history_data_test[0]

        event_widget_test = under_test.get_event_widget('hostname', event_test)

        self.assertIsInstance(event_widget_test, QWidget)
        self.assertEqual('history', event_widget_test.objectName())

    def test_get_icon_label(self):
        """Get History Icon QLabel"""

        under_test = HistoryQWidget.get_icon_label(self.history_data_test[0])

        self.assertEqual(QSize(32, 32), under_test.size())
        self.assertIsInstance(under_test, QLabel)

    def test_get_event_type(self):
        """Get Event History Type """

        under_test = HistoryQWidget.get_event_type(self.history_data_test[0], 'hostname')

        self.assertEqual('Service: Load', under_test)

        under_test = HistoryQWidget.get_event_type(self.history_data_test[2], 'hostname')

        self.assertEqual('Host: Hostname', under_test)
