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

from PyQt5.Qt import QApplication

from alignak_app.qobjects.dock.spy import SpyQWidget, SpyQListWidget, EventItem


class TestDataManager(unittest2.TestCase):
    """
        This file test the SpyQWidget, SpyQListWidget classes.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize SpyQWidget"""

        under_test = SpyQWidget()

        self.assertIsNotNone(under_test.spy_list_widget)
        self.assertIsInstance(under_test.spy_list_widget, SpyQListWidget)
        self.assertIsNone(under_test.spy_list_widget.item(0))

        under_test.initialize()

        self.assertIsNotNone(under_test.spy_list_widget)
        self.assertIsInstance(under_test.spy_list_widget, SpyQListWidget)
        self.assertIsNotNone(under_test.spy_list_widget.item(0))

    def test_remove_event(self):
        """Remove Spy Event Item"""

        under_test = SpyQWidget()
        under_test.initialize()

        spy_item_test = EventItem()
        spy_item_test.initialize('OK', 'Message', spied_on=True, host='_id_1')

        self.assertIsNone(under_test.spy_list_widget.item(1))

        under_test.spy_list_widget.addItem(spy_item_test)

        # Assert EventItem is same that the one added
        self.assertEqual(spy_item_test, under_test.spy_list_widget.item(1))

        # Set this item to current one and add it to spy list
        under_test.spy_list_widget.setCurrentItem(under_test.spy_list_widget.item(1))
        under_test.spy_list_widget.spied_hosts.append('_id_1')

        under_test.remove_event()

        # Event is no more here
        self.assertIsNone(under_test.spy_list_widget.item(1))