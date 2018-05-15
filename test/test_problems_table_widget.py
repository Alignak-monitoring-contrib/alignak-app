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

import unittest2

from PyQt5.Qt import QStandardItem

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service

from alignak_app.qobjects.alignak.problems_table import ProblemsQTableView


class TestProblemsQTableView(unittest2.TestCase):
    """
        This file test the ProblemsQTableView class.
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
                '_id': '_id%d' % i,
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

    def test_initialize_tables_problems(self):
        """Initialize ProblemsQTableWidget"""

        problems = data_manager.get_problems()
        under_test = ProblemsQTableView()
        self.assertIsNone(under_test.model())
        self.assertIsNone(under_test.selectionModel())

        under_test.update_view(problems)

        self.assertIsNotNone(under_test.model())
        self.assertIsNotNone(under_test.selectionModel())

        self.assertEqual(['Items in problem', 'Output'], under_test.headers_list)
        self.assertEqual(2, under_test.model().columnCount())

    def test_get_tableitem(self):
        """Get Problems Table Item"""

        under_test = ProblemsQTableView()
        tableitem_test = under_test.get_tableitem(self.host_list[0])

        self.assertIsInstance(tableitem_test, QStandardItem)
        self.assertEqual('Host 0 is UNKNOWN', tableitem_test.text())

        tableitem_test = under_test.get_tableitem(self.service_list[0])

        self.assertIsInstance(tableitem_test, QStandardItem)
        self.assertEqual('Service 0 is CRITICAL (Attached to Host 0)', tableitem_test.text())
