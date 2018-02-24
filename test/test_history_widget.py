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
from PyQt5.QtWidgets import QApplication, QWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.history import History
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.panel.history import HistoryQWidget, AppQFrame

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
            'service_name': 'Memory',
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

        data_manager.database['history'].append(self.history_test)
        under_test.initialize('charnay', self.history_test)

        self.assertIsNotNone(under_test.layout())
        self.assertEqual(under_test.app_widget.windowTitle(), "History of Charnay")

    def test_get_event_widget(self):
        """Get Event QWidget"""

        hist_widget_test = HistoryQWidget()

        under_test = hist_widget_test.get_history_widget_model(self.history_test.data[0], 'Load')

        self.assertTrue("ack.processed" in under_test.toolTip())
        self.assertIsNotNone(under_test.layout())
        self.assertIsInstance(under_test, QWidget)
