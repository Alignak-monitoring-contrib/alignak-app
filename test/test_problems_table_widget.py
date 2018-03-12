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

from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.alignak.problems_table import AppQTableWidgetItem, ProblemsQTableWidget
from alignak_app.qobjects.events.spy import SpyQWidget


class TestProblemsQTableWidget(unittest2.TestCase):
    """
        This file test the ProblemsQTableWidget class.
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

    def test_initialize_tables_problems(self):
        """Initialize ProblemsQTableWidget"""

        under_test = ProblemsQTableWidget()

        self.assertEqual(
            ['Items in problem', 'Output'],
            under_test.headers_list
        )
        self.assertEqual(0, under_test.columnCount())

    def test_get_tableitem(self):
        """Get Problems Table Item"""

        under_test = ProblemsQTableWidget()
        tableitem_test = under_test.get_tableitem(self.host_list[0])

        self.assertIsInstance(tableitem_test, AppQTableWidgetItem)
        self.assertEqual('Host 0 is UNKNOWN', tableitem_test.text())

        tableitem_test = under_test.get_tableitem(self.service_list[0])

        self.assertIsInstance(tableitem_test, AppQTableWidgetItem)
        self.assertEqual('Service 0 is CRITICAL (Attached to Host 0)', tableitem_test.text())
