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

from PyQt5.Qt import QApplication, QWidget

from alignak_app.items.host import Host

from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.alignak.problems_table import AppQTableWidgetItem
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
                'ls_downtimed': True,
                'ls_acknowledged': True,
                'ls_state': 'UNKNOWN',
                'ls_output': 'output host %d' % i
            },
            'host%d' % i
        )
        host_list.append(host)

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

        under_test.initialize(None)

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problem_table)
        self.assertTrue(under_test.problems_title)

        self.assertEqual('itemtitle', under_test.problems_title.objectName())

    def test_get_problems_widget_title(self):
        """Get problems Widget Title"""

        problems_widget_test = ProblemsQWidget()

        under_test = problems_widget_test.get_problems_widget_title()

        self.assertIsInstance(under_test, QWidget)

    def test_add_spy_host(self):
        """Add Psy Host from Problems QWidget"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        # Set a current item
        tableitem_test = AppQTableWidgetItem()
        tableitem_test.add_backend_item(self.host_list[0])
        under_test.problem_table.setItem(0, 0, tableitem_test)
        under_test.problem_table.setCurrentItem(tableitem_test)

        self.assertFalse(under_test.spy_widget.spy_list_widget.spied_hosts)

        under_test.add_spied_host()

        # Assert host has been spied
        self.assertTrue(under_test.spy_widget.spy_list_widget.spied_hosts)
        self.assertTrue(
            self.host_list[0].item_id in under_test.spy_widget.spy_list_widget.spied_hosts
        )

    def test_update_problems_data(self):
        """Update Problems Data"""

        under_test = ProblemsQWidget()
        spy_widget_test = SpyQWidget()
        spy_widget_test.initialize()
        under_test.initialize(spy_widget_test)

        host_tableitem_test = under_test.problem_table.takeItem(0, 0)
        output_tableitem_test = under_test.problem_table.takeItem(0, 1)

        under_test.update_problems_data()

        # Assert Table items and QWidgets have changed
        self.assertNotEqual(host_tableitem_test, under_test.problem_table.takeItem(0, 0))
        self.assertNotEqual(output_tableitem_test, under_test.problem_table.takeItem(0, 1))
