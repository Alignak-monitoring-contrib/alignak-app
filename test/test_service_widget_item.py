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

from alignak_app.synthesis.service_widget_item import ServiceListWidgetItem

from PyQt5.QtWidgets import QApplication


class TestServiceListWidgetItem(unittest2.TestCase):
    """
        This file test the ServiceListWidgetItem class.
    """

    service_aggregation = {
        'display_name': 'My Service',
        'ls_state': 'OK',
        'ls_acknowledged': True,
        'ls_downtimed': False,
        'aggregation': 'Health',
    }

    service_no_aggregation = {
        'display_name': 'My Second Service',
        'ls_state': 'UNKNOWN',
        'ls_acknowledged': False,
        'ls_downtimed': True,
        'aggregation': '',
    }

    service_ack_down_false = {
        'display_name': 'My Second Service',
        'ls_state': 'CRITICAL',
        'ls_acknowledged': False,
        'ls_downtimed': False,
        'aggregation': '',
    }

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize ServiceListWidgetItem"""

        under_test = ServiceListWidgetItem()
        self.assertFalse(under_test.aggregation)
        self.assertFalse(under_test.state)
        self.assertEqual('', under_test.text())

        under_test.initialize(self.service_aggregation)

        self.assertTrue(under_test.aggregation)
        self.assertEqual('Health', under_test.aggregation)

        self.assertTrue(under_test.state)
        self.assertEqual('ACKNOWLEDGE', under_test.state)

        self.assertEqual('My service is OK', under_test.text())

    def test_aggregation_none_is_global(self):
        """ServiceListWidgetItem aggregation None becomes Global"""

        under_test = ServiceListWidgetItem()
        self.assertFalse(under_test.aggregation)
        self.assertFalse(under_test.state)

        self.assertEqual('', under_test.text())

        under_test.initialize(self.service_no_aggregation)

        self.assertFalse(under_test.aggregation)
        self.assertEqual('', under_test.aggregation)

        self.assertTrue(under_test.state)
        self.assertEqual('DOWNTIME', under_test.state)

        self.assertEqual('My second service is UNKNOWN', under_test.text())

    def test_if_ack_and_down_false_get_state(self):
        """ServiceListWidgetItem ack and down false, get state"""

        under_test = ServiceListWidgetItem()
        under_test.initialize(self.service_ack_down_false)

        self.assertTrue(under_test.state)
        self.assertEqual('CRITICAL', under_test.state)

    def test_get_service_tooltip(self):
        """ServiceListWidgetItem get service tooltip"""

        under_test = ServiceListWidgetItem()
        under_test.initialize(self.service_aggregation)

        tooltip_test = under_test.get_service_tooltip(self.service_aggregation)

        self.assertEqual('My service is OK and acknowledged !', tooltip_test)

        tooltip_test = under_test.get_service_tooltip(self.service_no_aggregation)
        self.assertEqual('My second service is UNKNOWN and downtimed !', tooltip_test)

        tooltip_test = under_test.get_service_tooltip(self.service_ack_down_false)
        self.assertEqual('My second service is CRITICAL', tooltip_test)
