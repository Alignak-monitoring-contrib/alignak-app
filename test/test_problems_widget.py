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
import os

import unittest2

from PyQt5.Qt import QApplication, QWidget, QTableWidgetItem

from alignak_app.items.host import Host
from alignak_app.items.service import Service
from alignak_app.backend.datamanager import data_manager

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.events.spy import SpyQWidget


class TestDataManager(unittest2.TestCase):
    """
        This file test the ProblemsQWidget class.
    """

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {
                'name': 'host%d' % i,
                'alias': 'Host %d' % i,
                '_id': '_id%d' % i,
                'ls_downtimed': True,
                'ls_acknowledged': True,
                'ls_state': 'UNKNOWN',
                'ls_output': 'output host %d' % i
            },
            'host%d' % i
        )
        host_list.append(host)

    # Service data test
    service_list = []
    for i in range(0, 10):
        service = Service()
        service.create(
            '_id%d' % i,
            {
                'name': 'service%d' % i,
                'alias': 'Service %d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'ls_output': 'output host %d' % i,
                'aggregation': 'disk',
                '_overall_state_id': 4
            },
            'service%d' % i
        )
        service_list.append(service)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize ProblemsQWidget"""

        under_test = ProblemsQWidget()

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problem_table)
        self.assertTrue(under_test.problems_title)
        self.assertTrue(under_test.headers_list)
        self.assertEqual(
            ['Item Type', '', 'Host', 'Service', 'State', 'Actions', 'Output'],
            under_test.headers_list
        )

        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)
        under_test.initialize(None)

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problem_table)
        self.assertTrue(under_test.problems_title)
        self.assertTrue(under_test.headers_list)
        self.assertEqual(
            ['Item Type', '', 'Host', 'Service', 'State', 'Actions', 'Output'],
            under_test.headers_list
        )
        self.assertEqual('itemtitle', under_test.problems_title.objectName())

    def test_get_problems_widget_title(self):
        """Get problems Widget Title"""

        problems_widget_test = ProblemsQWidget()

        under_test = problems_widget_test.get_problems_widget_title()

        self.assertIsInstance(under_test, QWidget)

    def test_get_icon_widget(self):
        """Get Problems Icon QWidget"""

        under_test = ProblemsQWidget.get_icon_widget(self.host_list[0])

        self.assertIsInstance(under_test, QWidget)

    def test_get_btn_widget(self):
        """Get Problems SPy Button QWidget"""

        under_test = ProblemsQWidget()

        spy_btn_test = under_test.get_btn_widget(self.service_list[0])

        self.assertIsInstance(spy_btn_test, QWidget)

    def test_get_tableitem(self):
        """Get Problems Table Item"""

        under_test = ProblemsQWidget.get_tableitem('test')

        self.assertIsInstance(under_test, QTableWidgetItem)
        self.assertEqual('test', under_test.text())

    def test_get_host_tableitem(self):
        """Get Host Table Item"""

        under_test = ProblemsQWidget.get_host_tableitem(self.host_list[0])

        self.assertIsInstance(under_test, QTableWidgetItem)
        self.assertEqual('Host 0', under_test.text())

    def test_get_service_tableitem(self):
        """Get Service Table Item"""

        under_test = ProblemsQWidget.get_service_tableitem(self.service_list[0])

        self.assertIsInstance(under_test, QTableWidgetItem)
        self.assertEqual('Service 0', under_test.text())

    def test_get_action_widget(self):
        """Get Problems Actions QWidget"""

        under_test = ProblemsQWidget.get_action_widget(self.host_list[0])

        self.assertIsInstance(under_test, ActionsQWidget)
        self.assertIsNotNone(under_test.item)

    def test_add_spy_host(self):
        """Add Psy Host from Problems QWidget"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        self.assertFalse(under_test.spy_widget.spy_list_widget.spied_hosts)

        under_test.add_spied_host(self.host_list[0].item_id)

        self.assertTrue(under_test.spy_widget.spy_list_widget.spied_hosts)

    def test_update_problems_data(self):
        """Update Problems Data"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        icon_widget_test = under_test.problem_table.cellWidget(0, 0)
        btn_widget_test = under_test.problem_table.cellWidget(0, 1)
        host_tableitem_test = under_test.problem_table.takeItem(0, 2)
        service_tableitem_test = under_test.problem_table.takeItem(0, 3)
        state_tableitem_test = under_test.problem_table.takeItem(0, 4)
        action_widget_test = under_test.problem_table.cellWidget(0, 5)
        output_tableitem_test = under_test.problem_table.takeItem(0, 6)

        under_test.update_problems_data()

        # Assert Table items and QWidgets have changed
        self.assertNotEqual(icon_widget_test, under_test.problem_table.cellWidget(0, 0))
        self.assertNotEqual(btn_widget_test, under_test.problem_table.cellWidget(0, 1))
        self.assertNotEqual(host_tableitem_test, under_test.problem_table.takeItem(0, 2))
        self.assertNotEqual(service_tableitem_test, under_test.problem_table.takeItem(0, 3))
        self.assertNotEqual(state_tableitem_test, under_test.problem_table.takeItem(0, 4))
        self.assertNotEqual(action_widget_test, under_test.problem_table.cellWidget(0, 5))
        self.assertNotEqual(output_tableitem_test, under_test.problem_table.takeItem(0, 6))
