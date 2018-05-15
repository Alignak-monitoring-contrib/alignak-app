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

from PyQt5.Qt import QApplication, QItemSelectionModel, Qt

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service

from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.events.spy import SpyQWidget


class TestProblemsQWidget(unittest2.TestCase):
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
                'ls_downtimed': False,
                'ls_acknowledged': False,
                'ls_state': 'DOWN',
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
                'host': '_id%d' % i,
                '_id': '_id%d' % i,
                'ls_state': 'CRITICAL',
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_output': 'output service %d' % i
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
        self.assertTrue(under_test.problems_table)
        self.assertTrue(under_test.problems_title)
        self.assertFalse(under_test.filter_hosts_btn.is_checked())
        self.assertFalse(under_test.filter_services_btn.is_checked())

        under_test.initialize(None)

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problems_table)
        self.assertTrue(under_test.problems_title)
        self.assertFalse(under_test.filter_hosts_btn.is_checked())
        self.assertFalse(under_test.filter_services_btn.is_checked())

        self.assertEqual('title', under_test.problems_title.objectName())

    def test_add_spy_host(self):
        """Add Spy Host from Problems QWidget"""

        data_manager.update_database('host', [])
        data_manager.update_database('service', [])

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        # Update view with problems
        under_test.problems_table.update_view({'problems': [self.host_list[8]]})

        # Make this QStandardItem as current index
        index_test = under_test.problems_table.model().index(0, 0)
        under_test.problems_table.selectionModel().setCurrentIndex(
            index_test,
            QItemSelectionModel.SelectCurrent
        )

        self.assertFalse(under_test.spy_widget.spy_list_widget.spied_hosts)

        under_test.add_spied_host()

        # Assert host has been spied
        self.assertTrue(under_test.spy_widget.spy_list_widget.spied_hosts)
        # "_id8" is inside "spied_hosts"
        self.assertTrue(
            self.host_list[8].item_id in under_test.spy_widget.spy_list_widget.spied_hosts
        )

    def test_update_problems_data(self):
        """Update Problems Data"""

        # Reset Problems
        data_manager.database['problems'] = []

        # Initialize QWidget
        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        model_test = under_test.problems_table.model()
        select_model_test = under_test.problems_table.selectionModel()

        under_test.update_problems_data()

        # Assert Table models have changed
        self.assertNotEqual(model_test, under_test.problems_table.model())
        self.assertNotEqual(select_model_test, under_test.problems_table.selectionModel())

        # Add problems
        for item in self.host_list:
            data_manager.database['problems'].append(item)
        for item in self.service_list:
            data_manager.database['problems'].append(item)

        # Assert filter buttons are False
        self.assertFalse(under_test.filter_hosts_btn.is_checked())
        self.assertFalse(under_test.filter_services_btn.is_checked())

        # Even if a filter is given,
        # the view does not filter by item type if filter buttons are False
        under_test.update_problems_data('service')

        # Collect items
        items_test = [
            under_test.problems_table.model().data(
                under_test.problems_table.model().index(row, 0), Qt.UserRole
            )
            for row in range(under_test.problems_table.model().rowCount())
        ]

        self.assertEqual(20, len(items_test))

    def test_update_problems_data_keep_linesearch_text(self):
        """Update Problems Data Keep LineSearch Text"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(None)

        self.assertFalse(under_test.line_search.text())

        # Set text of QLineEdit
        under_test.line_search.setText('research')

        under_test.update_problems_data()

        # After update, text is keeped
        self.assertEqual('research', under_test.line_search.text())

    def test_filter_hosts(self):
        """Filter Hosts in Problems View"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        # Add problems
        data_manager.database['problems'] = []
        for item in self.host_list:
            data_manager.database['problems'].append(item)
        for item in self.service_list:
            data_manager.database['problems'].append(item)

        # Update and filter Hosts
        under_test.filter_hosts_btn.update_btn_state(True)
        under_test.update_problems_data('host')

        # Assert service filter button is False
        self.assertFalse(under_test.filter_services_btn.is_checked())
        # Collect items
        items_test = [
            under_test.problems_table.model().data(
                under_test.problems_table.model().index(row, 0), Qt.UserRole
            )
            for row in range(under_test.problems_table.model().rowCount())
        ]

        self.assertEqual(10, len(items_test))
        for item in items_test:
            self.assertIsInstance(item, Host)

    def test_filter_services(self):
        """Filter Services in Problems View"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        # Update and filter Services
        under_test.filter_services_btn.update_btn_state(True)
        under_test.update_problems_data('service')

        # Assert host filter button is False
        self.assertFalse(under_test.filter_hosts_btn.is_checked())
        # Collect items
        items_test = [
            under_test.problems_table.model().data(
                under_test.problems_table.model().index(row, 0), Qt.UserRole
            )
            for row in range(under_test.problems_table.model().rowCount())
        ]

        self.assertEqual(10, len(items_test))
        for item in items_test:
            self.assertIsInstance(item, Service)
